from nose.tools import nottest

from notifications.models import connection
from notifications.services import BillService, VoteService, BillActionService
from dateutil.parser import parse as parse_date

from bson.objectid import ObjectId

TEST_DATABASE = 'norrinTests'

class TestNorrin:

    def setup(self):
        self.connection = connection
        self.db = self.connection[TEST_DATABASE]

    def teardown(self):
        # self.connection.drop_database(self.db)
        pass

    @nottest
    def bill_test_dict(self):
        return {
            'bill_id': u's1822-113',
            'sponsor_id': u'D000563',
            'introduced_on': u'2013-12-12'
        }

    def test_bill(self):
        obj = self.db.Bill()
        data = self.bill_test_dict()
        obj.bill_id = data['bill_id']
        obj.sponsor_id = data['sponsor_id']
        obj.introduced_on = parse_date(data['introduced_on'])
        obj.save()
        assert isinstance(obj['_id'], ObjectId)

    def test_bill_update(self):
        obj = self.db.Bill(self.bill_test_dict())
        obj.save()

    def test_billservice(self):
        BillService(database=self.db).run()
        assert self.db.bills.count() > 0

    def test_voteservice(self):
        VoteService(database=self.db).run()
        assert self.db.votes.count() > 0

    def test_billactionservice(self):
        BillActionService(database=self.db).run()
        assert self.db.bill_actions.count() > 0
