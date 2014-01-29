from nose.tools import nottest
import logging

import os

import json

from mongokit import ObjectId

from norrin.notifications.models import connection
from norrin.notifications.services import BillService, VoteService, \
    BillActionService, adapters

from sunlight import congress
from dateutil.parser import parse as parse_date
import urbanairship as ua

TEST_DATABASE = 'norrinTests'
PRESERVE_TEST_DB = os.environ.get('PRESERVE_TEST_DB', False)

logger = logging.getLogger(__name__)


class InspectNotificationAdapter(object):
    def __init__(self):
        self.payloads = []

    def push(self, notification):
        pyld_json = json.dumps(ua.notification(ios=ua.ios(alert=notification.message, extra=notification.context)))
        self.payloads.append(pyld_json)

def teardown(self):
    if PRESERVE_TEST_DB:
        logger.warning('Preserving test database...')
    else:
        logger.warning('Dropping test database...')
        connection.drop_database(TEST_DATABASE)


class DBConnected(object):
    """docstring for Base"""
    def __init__(self):
        self.db = connection[TEST_DATABASE]


class TestBills(DBConnected):

    def setup(self):
        self.service = BillService(self.db)
        self.service.load_data()

        if self.db.bills.count() == 0:
            last_bills = congress.bills(order='introduced_on', fields='bill_id,sponsor_id,introduced_on', per_page=20)
            for bill in last_bills:
                obj = self.db.Bill()
                obj.bill_id = bill['bill_id']
                obj.sponsor_id = bill['sponsor_id']
                obj.introduced_on = parse_date(bill['introduced_on'])
                obj.save()

    @nottest
    def bill_dict(self):
        return {
            'bill_id': u's1822-113',
            'sponsor_id': u'D000563',
            'introduced_on': u'2013-12-12'
        }

    @nottest
    def bill_update_dict(self):
        return {
            'processed': True,
            'introduced_on': parse_date(u'2010-12-12')
        }

    def test_1billservice(self):
        '''Test for presence of bills in db'''
        assert self.db.bills.count() > 0

    def test_bill(self):
        '''Test bill creation & saving'''
        obj = self.db.Bill()
        data = self.bill_dict()
        obj.bill_id = data['bill_id']
        obj.sponsor_id = data['sponsor_id']
        obj.introduced_on = parse_date(data['introduced_on'])
        obj.save()
        assert isinstance(obj['_id'], ObjectId)

    def test_bill_update(self):
        '''Update a random bill'''
        obj = self.db.Bill.find_random()
        obj.update(self.bill_update_dict())
        obj.save()
        assert obj.bill_id != False

    def test_bill_notification_size(self):
        '''Check size of notification payloads for APNS using the InspectNotificationAdapter'''
        adapter = InspectNotificationAdapter()
        adapters.register(adapter)
        self.service.run()
        logger.warning('Checking payloads')
        for payload in adapter.payloads:
            pyld_len = len(payload.encode('utf-8'))
            logger.warning(u'Payload length: {}'.format(pyld_len))
            assert pyld_len <= 256


class TestBillActions(DBConnected):

    def setup(self):
        BillActionService(self.db).load_data()

    def test_1billactionservice(self):
        '''Test for presence of bill actions in db'''
        assert self.db.bill_actions.count() > 0


class TestVotes(DBConnected):

    def setup(self):
        VoteService(self.db).load_data()

    def test_1voteservice(self):
        '''Test for presence of votes in db'''
        assert self.db.votes.count() > 0


# class TestUtils(object):

#     def test_day_before(self):
#         pass
