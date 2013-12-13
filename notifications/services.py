from datetime import timedelta
import logging
from collections import defaultdict

import urbanairship as ua
from dateutil.parser import parse as parse_date
from sunlight import congress

import config
from notifications.adapters import ConsoleAdapter, UrbanAirshipAdapter, MongoDBAdapter
from notifications.models import connection
from util import day_before, yesterday, format_billid

logger = logging.getLogger('norrin.notifications')
airship = ua.Airship(config.UA_KEY, config.UA_MASTER)

ADAPTERS = [
    ConsoleAdapter(),
    # UrbanAirshipAdapter(airship),
    MongoDBAdapter(connection[config.MONGODB_DATABASE]),
]


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

    # lifecycle methods

    def start(self):
        logger.info('reloading subscribers')
        self.reload_subscribers()

    def load_data(self):
        return NotImplementedError('load_data must be implemented by the subclass')

    def send_notifications(self):
        return NotImplementedError('send_notifications must be implemented by the subclass')

    def push_notification(self, notification):
        for adapter in ADAPTERS:
            adapter.push(notification)

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
        self.start()
        self.load_data()
        self.send_notifications()
        self.finish()


class BillService(Service):

    def load_data(self):

        res = self.db.bills.aggregate({'$group': {'_id': '', 'last': {'$max': '$introduced_on'}}})
        since = res['result'][0]['last'] if res['result'] else yesterday()

        count = 0

        for bill in congress.bills(introduced_on__gte=since.date().isoformat(), fields='bill_id,sponsor_id,introduced_on', per_page=50):
            if self.db.bills.find_one({'bill_id': bill['bill_id']}) is None:
                obj = self.db.Bill(bill)
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

            self.push_notification(notification)

    # def finish(self):
    #     self.db.bills.update({'processed': False}, {'$set': {'processed': True}})


class VoteService(Service):

    def load_data(self):

        res = self.db.votes.aggregate({'$group': {'_id': '', 'last': {'$max': '$voted_at'}}})
        since = res['result'][0]['last'] if res['result'] else day_before(yesterday())

        since = yesterday() - timedelta(days=16)

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

                    self.push_notification(notification)

                    # push = airship.create_push()
                    # push.audience = ua.tag('/bills/%s' % vote.bill_id)
                    # push.notification = ua.ios(alert=msg)
                    # push.device_types = ua.all_
                    # push.send()


class BillActionService(Service):

    def load_data(self):

        res = self.db.bill_actions.aggregate({'$group': {'_id': '', 'last': {'$max': '$acted_at'}}})
        since = res['result'][0]['last'] if res['result'] else yesterday(5)

        for bill in congress.bills(introduced_on__gte=since.isoformat(), fields='bill_id,actions', per_page=50):
            for action in bill['actions']:
                action['acted_at'] = parse_date(action['acted_at'])

                if self.db.votes.find_one({'bill_id': bill['bill_id'], 'acted_at': action['acted_at'], 'type': action['type']}) is None:
                    obj = self.db.BillAction()
                    obj.bill_id = bill['bill_id']
                    obj.acted_at = action['acted_at']
                    obj.type = action['type']
                    obj.roll_id = action.get('roll_id')
                    if 'committees' in action:
                        obj.committee_ids = sorted(c['committee_id'] for c in action['committees'])
                    obj.save()

    def send_notifications(self):
        pass
