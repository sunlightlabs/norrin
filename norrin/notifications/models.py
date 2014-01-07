from datetime import datetime
from mongokit import Connection, Document

from norrin import config

connection = Connection(config.MONGODB_HOST, config.MONGODB_PORT)
if config.MONGODB_USERNAME and config.MONGODB_PASSWORD:
    connection[config.MONGODB_DATABASE].authenticate(config.MONGODB_USERNAME, config.MONGODB_PASSWORD)

@connection.register
class Bill(Document):
    __collection__ = 'bills'
    structure = {
        'bill_id': unicode,
        'sponsor_id': unicode,
        'introduced_on': datetime,
        'timestamp': datetime,
        'processed': bool,
    }
    required_fields = ['bill_id', 'sponsor_id', 'introduced_on']
    default_values = {'timestamp': datetime.utcnow, 'processed': False}
    use_dot_notation = True


@connection.register
class BillAction(Document):
    __collection__ = 'bill_actions'
    structure = {
        'bill_id': unicode,
        'type': unicode,
        'acted_at': datetime,
        'roll_id': unicode,
        'committee_ids': list,
        'timestamp': datetime,
        'processed': bool,
    }
    required_fields = ['bill_id', 'type', 'acted_at']
    default_values = {'timestamp': datetime.utcnow, 'processed': False}
    use_dot_notation = True


@connection.register
class Vote(Document):
    __collection__ = 'votes'
    structure = {
        'roll_id': unicode,
        'type': unicode,
        'bill_id': unicode,
        'sponsor_id': unicode,
        'voted_at': datetime,
        'result': unicode,
        'timestamp': datetime,
        'processed': bool,
    }
    required_fields = ['roll_id', 'type']
    default_values = {'timestamp': datetime.utcnow, 'processed': False}
    use_dot_notation = True


@connection.register
class UpcomingBill(Document):
    __collection__ = 'upcoming_bills'
    structure = {
        'bill_id': unicode,
        'sponsor_id': unicode,
        'legislative_day': datetime,
        'timestamp': datetime,
        'processed': bool,
    }
    required_fields = ['bill_id', 'sponsor_id', 'legislative_day']
    default_values = {'timestamp': datetime.utcnow, 'processed': False}
    use_dot_notation = True


@connection.register
class Subscriber(Document):
    __collection__ = 'subscribers'
    structure = {
        'id': unicode,
        'type': unicode,
        'active': bool,
        'tags': list,
        'alias': unicode,
        'timestamp': datetime,
    }
    required_fields = ['id', 'type', 'active']
    default_values = {'timestamp': datetime.utcnow}
    use_dot_notation = True

    def followed_bills(self):
        return [f[7:] for f in self.favorites if f.startswith('/bills')]

    def followed_committees(self):
        return [f[12:] for f in self.favorites if f.startswith('/committees')]

    def followed_legislators(self):
        return [f[12:] for f in self.favorites if f.startswith('/legislators')]


@connection.register
class Notification(Document):
    __collection__ = 'notifications'
    structure = {
        'id': unicode,
        'type': unicode,
        'message': unicode,
        'payload': dict,
        'timestamp': datetime,
    }
    required_fields = ['id', 'type', 'message', 'timestamp']
    default_values = {'timestamp': datetime.utcnow}
    use_dot_notation = True
