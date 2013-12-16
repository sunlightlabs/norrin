from nose.tools import nottest

from mongokit import ObjectId

from notifications.models import connection
from notifications.services import BillService, VoteService, BillActionService

import datetime
from dateutil.parser import parse as parse_date

TEST_DATABASE = 'norrinTests'

class DBConnected(object):
    """docstring for Base"""
    def __init__(self):
        self.db = connection[TEST_DATABASE]

class TestBills(DBConnected):

    def setup(self):
        BillService(self.db).run()

    @nottest
    def bill_dict(self):
        return {
            'bill_id': u's1822-113',
            'sponsor_id': u'D000563',
            'introduced_on': parse_date(u'2013-12-12')
        }

    @nottest
    def bill_update_dict(self):
        return {
            'processed': True
        }

    def test_bill(self):
        obj = self.db.Bill()
        data = self.bill_dict()
        obj.bill_id = data['bill_id']
        obj.sponsor_id = data['sponsor_id']
        obj.introduced_on = data['introduced_on']
        obj.save()
        assert isinstance(obj['_id'], ObjectId)

    def test_bill_update(self):
        obj = self.db.Bill()
        obj.update(self.bill_update_dict())
        obj.save()
        assert obj.bill_id != False

    def test_billservice(self):
        assert self.db.bills.count() > 0


class TestBillActions(DBConnected):

    def setup(self):
        BillActionService(self.db).run()

    def test_billactionservice(self):
        assert self.db.bill_actions.count() > 0


class TestVotes(DBConnected):

    def setup(self):
        VoteService(self.db).run()

    def test_voteservice(self):
        assert self.db.votes.count() > 0


# class TestUtils(object):

#     def test_day_before(self):
#         pass
