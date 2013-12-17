from nose.tools import nottest

from mongokit import ObjectId

from notifications.models import connection
from notifications.services import BillService, VoteService, BillActionService

import config
from util import yesterday, day_before
from dateutil.parser import parse as parse_date

TEST_DATABASE = 'norrinTests'

SINCE_DATE = parse_date(config.LOAD_SINCE_DATE) if config.LOAD_SINCE_DATE else day_before(yesterday())

def tearDownModule(self):
    if not config.PRESERVE_TEST_DB:
        connection.drop_database(TEST_DATABASE)


class DBConnected(object):

    def __init__(self):
        self.db = connection[TEST_DATABASE]


class TestBills(DBConnected):

    def setup(self):
        print("Load since {0}".format(SINCE_DATE))
        BillService(database=self.db).load_data(since=SINCE_DATE)

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


class TestBillActions(DBConnected):

    def setup(self):
        BillActionService(database=self.db).load_data(since=SINCE_DATE)

    def test_1billactionservice(self):
        '''Test for presence of bill actions in db'''
        assert self.db.bill_actions.count() > 0


class TestVotes(DBConnected):

    def setup(self):
        VoteService(database=self.db).load_data(since=SINCE_DATE)

    def test_1voteservice(self):
        '''Test for presence of votes in db'''
        assert self.db.votes.count() > 0


# class TestUtils(object):

#     def test_day_before(self):
#         pass
