import datetime
import logging
from collections import defaultdict

import urbanairship as ua
from dateutil.parser import parse as parse_date
from sunlight import congress
from raven import Client as Raven

from . import config
from .models import connection
from norrin.util import day_before, yesterday, format_billid

logger = logging.getLogger('norrin.notifications')
airship = ua.Airship(config.UA_KEY, config.UA_MASTER)


class AdapterRegistry(object):

    def __init__(self):
        self._adapters = []

    def __iter__(self):
        for adapter in self._adapters:
            yield adapter

    def register(self, adapter):
        if isinstance(adapter, type):
            adapter = adapter()
        if adapter not in self._adapters:
            self._adapters.append(adapter)

    def deregister(self, adapter):
        if adapter in self._adapters:
            self._adapters.remove(adapter)

    def reset(self):
        self._adapters[:] = []

adapters = AdapterRegistry()


class Notification(object):

    def __init__(self, type, message=None, tags=None):
        self.type = type
        self.message = message
        self.tags = tags or []
        self.context = {}
        self.scheduled_for = None


class Service(object):

    def __init__(self, database=None):
        self.db = database or connection[config.MONGODB_DATABASE]
        self.sentry = Raven(config.SENTRY_DSN) if config.SENTRY_DSN else None

    # lifecycle methods

    def start(self):
        if config.AUTORELOAD_SUBSCRIBERS:
            logger.info('autoreloading subscribers')
            self.reload_subscribers()
        else:
            logger.info('skipping autoreloading subscribers')

    def load_data(self, since=None):
        return NotImplementedError('load_data must be implemented by the subclass')

    def send_notifications(self):
        return NotImplementedError('send_notifications must be implemented by the subclass')

    def push_notification(self, notification):
        for adapter in adapters:
            try:
                adapter.push(notification)
            except:
                if self.sentry:
                    self.sentry.captureException()

    def finish(self):
        pass

    # action methods

    def reload_subscribers(self):
        self.db.subscribers.remove({})
        for dt in ua.DeviceTokenList(airship):
            if dt.active:
                subscriber = self.db.Subscriber()
                subscriber.id = unicode(dt.id)
                subscriber.type = unicode(dt.device_type)
                subscriber.active = dt.active
                subscriber.tags = dt.tags or []
                subscriber.alias = unicode(dt.alias) if dt.alias else None
                subscriber.save()

    def run(self):
        try:
            self.start()
            self.load_data()
            self.send_notifications()
            self.finish()
        except:
            if self.sentry:
                self.sentry.captureException()


class BillService(Service):

    def load_data(self, since=None):

        if not since:
            res = self.db.bills.aggregate({'$group': {'_id': '', 'last': {'$max': '$introduced_on'}}})
            since = res['result'][0]['last'] if res['result'] else yesterday()

        count = 0

        for bill in congress.bills(introduced_on__gte=since.date().isoformat(), fields='bill_id,sponsor_id,introduced_on', per_page=50):
            if self.db.bills.find_one({'bill_id': bill['bill_id']}) is None:
                obj = self.db.Bill()
                obj.bill_id = bill['bill_id']
                obj.sponsor_id = bill['sponsor_id']
                obj.introduced_on = parse_date(bill['introduced_on'])
                obj.save()

                count += 1

        logger.info('loaded %d bills' % count)

    def send_notifications(self):

        sponsors = defaultdict(list)

        for bill in list(self.db.Bill.find({'processed': False})):
            sponsors[bill['sponsor_id']].append(bill)

        for sponsor_id, bills in sponsors.items():

            sponsor = congress.legislators(bioguide_id=sponsor_id)[0]
            name = "%s. %s %s" % (sponsor['title'], sponsor['first_name'], sponsor['last_name'])

            bill_count = len(bills)

            if bill_count == 1:
                msg = "%s sponsored a bill" % name
            else:
                msg = "%s sponsored %s bills" % (name, bill_count)

            notification = Notification('/legislator/sponsor/introduced')
            notification.message = msg
            notification.tags = ['/legislators/%s' % sponsor_id]
            notification.context = {
                'type': notification.type,
                'legislator': sponsor_id,
                'bills': [b['bill_id'] for b in bills],
            }

            if bill_count == 1:
                notification.context['app_url'] = '/bills/%s' % bills[0]['bill_id']
            else:
                notification.context['app_url'] = '/legislators/%s/sponsored' % sponsor_id

            self.push_notification(notification)

    def finish(self):
        self.db.bills.update({'processed': False}, {'$set': {'processed': True}}, multi=True)


class VoteService(Service):

    def load_data(self, since=None):

        if not since:
            res = self.db.votes.aggregate({'$group': {'_id': '', 'last': {'$max': '$voted_at'}}})
            since = res['result'][0]['last'] if res['result'] else day_before(yesterday())

        votes = congress.votes(voted_at__gte=since.isoformat() + 'Z', fields='roll_id,vote_type,bill,voted_at,result', per_page=50)

        for vote in votes:
            if self.db.votes.find_one({'roll_id': vote['roll_id']}) is None:
                obj = self.db.Vote()
                obj.roll_id = vote['roll_id']
                obj.type = vote['vote_type']
                obj.voted_at = parse_date(vote['voted_at'])
                obj.result = vote['result']
                if 'bill' in vote:
                    obj.bill_id = vote['bill']['bill_id']
                    obj.sponsor_id = vote['bill']['sponsor_id']
                obj.save()

    def send_notifications(self):

        votes = list(self.db.Vote.find({'processed': False}))

        # logger.info('vote notifications for %d votes' % len(votes))

        for vote in votes:
            if vote.type in ('cloture', 'passage') and vote.bill_id:

                if vote.type in ('cloture', 'passage'):

                    msg = "%s vote on %s: %s" % (vote.type.title(), format_billid(vote.bill_id), vote.result)

                    notification = Notification('/bill/vote')
                    notification.message = msg
                    notification.tags = ['/bills/%s' % vote.bill_id]
                    notification.context = {
                        'vote': vote.roll_id,
                        'app_url': '/bills/%s/activity' % vote.bill_id,
                        'bill': vote.bill_id,
                    }

                    self.push_notification(notification)

    def finish(self):
        self.db.votes.update({'processed': False}, {'$set': {'processed': True}}, multi=True)


class BillActionService(Service):

    def load_data(self, since=None):

        if not since:
            res = self.db.bill_actions.aggregate({'$group': {'_id': '', 'last': {'$max': '$acted_at'}}})
            since = res['result'][0]['last'] if res['result'] else yesterday()

        for bill in congress.bills(last_action_at__gte=since.date().isoformat(), fields='bill_id,actions', per_page=50):
            for action in bill['actions']:
                action['acted_at'] = parse_date(action['acted_at'])

                if self.db.bill_actions.find_one({'bill_id': bill['bill_id'], 'acted_at': action['acted_at'], 'type': action['type']}) is None:

                    obj = self.db.BillAction()
                    obj.bill_id = bill['bill_id']
                    obj.acted_at = action['acted_at']
                    obj.type = action['type']
                    obj.roll_id = action.get('roll_id')
                    if 'committees' in action:
                        obj.committee_ids = sorted(c['committee_id'] for c in action['committees'])
                    obj.save()

    def send_notifications(self):

        actions = list(self.db.BillAction.find({'processed': False}))

        for action in actions:

            if action.type in ('veto', 'enacted', 'signed'):

                print action['type']

                if action.type == 'veto':
                    msg = '%s was vetoed by the President' % format_billid(action.bill_id)
                elif action.type == 'enacted':
                    msg = '%s was enacted into law' % format_billid(action.bill_id)
                elif action.type == 'signed':
                    msg = '%s was signed by the President' % format_billid(action.bill_id)

                notification = Notification('/bill/action')
                notification.message = msg
                notification.tags = ['/bills/%s' % action.bill_id]
                notification.context = {
                    'app_url': '/bills/%s/activity' % action.bill_id,
                    'vote': action.roll_id,
                    'bill': action.bill_id,
                    'action_type': action.type
                }

                self.push_notification(notification)

    def finish(self):
        self.db.bill_actions.update({'processed': False}, {'$set': {'processed': True}}, multi=True)


class UpcomingBillService(Service):

    def load_data(self, since=None):

        if not since:
            res = self.db.upcoming_bills.aggregate({'$group': {'_id': '', 'last': {'$max': '$legislative_day'}}})
            since = res['result'][0]['last'] if res['result'] else yesterday()

        for bill in congress.upcoming_bills(legislative_day__gte=since.date().isoformat(), fields='bill_id,legislative_day,range', per_page=50):
            if bill['legislative_day']:
                bill['legislative_day'] = parse_date(bill['legislative_day'])
                if self.db.upcoming_bills.find_one({'bill_id': bill['bill_id'], 'legislative_day': bill['legislative_day']}) is None:
                    obj = self.db.UpcomingBill()
                    obj.bill_id = bill['bill_id']
                    obj.legislative_day = bill['legislative_day']
                    obj.range = bill['range']
                    obj.save()

    def send_notifications(self):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0, 0, 0))
        bills = list(self.db.UpcomingBill.find({'processed': False, 'legislative_day': today}))

        for bill in bills:

            if bill['range'] == 'day':
                msg = '%s is scheduled for a vote today' % format_billid(bill.bill_id)
            elif bill['range'] == 'week':
                msg = '%s is scheduled for a vote this week' % format_billid(bill.bill_id)

            notification = Notification('/bill/upcoming')
            notification.message = msg
            notification.tags = ['/bills/%s' % bill.bill_id]
            notification.context = {
                'app_url': '/bills/%s' % bill.bill_id,
                'bill': bill.bill_id,
                'legislative_day': today.date().isoformat(),
            }

            self.push_notification(notification)

    def finish(self):
        self.db.upcoming_bills.update({'processed': False}, {'$set': {'processed': True}}, multi=True)
