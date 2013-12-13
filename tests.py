from notifications.models import connection
from notifications.services import BillService, VoteService, BillActionService
from dateutil.parser import parse as parse_date

TEST_DATABASE = 'norrinTests'

class TestNorrin:

    def setup(self):
        self.connection = connection
        self.db = self.connection[TEST_DATABASE]

    def teardown(self):
        # self.connection.drop_database(self.db)
        pass

    def test_bill(self):
        obj = self.db.Bill()
        obj.bill_id = u's1822-113'
        obj.sponsor_id = u'D000563'
        obj.introduced_on = parse_date(u'2013-12-12')
        obj.save()

    def test_billservice(self):
        BillService(self.db).run()
        assert self.db.bills.count() > 0

    def test_voteservice(self):
        VoteService(self.db).run()
        assert self.db.votes.count() > 0

    def test_billactionservice(self):
        BillActionService(self.db).run()
        assert self.db.bill_actions.count() > 0
