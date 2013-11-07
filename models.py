from datetime import datetime

from flask.ext.mongokit import Document


class Entity(Document):
    __collection__ = 'entities'
    structure = {
        'uuid': unicode,
        'type': unicode,
        'remote_id': unicode,
        'handled': bool,
        'creation': datetime,
        'data': dict,
    }
    required_fields = ['uuid', 'type', 'remote_id', 'handled', 'creation']
    default_values = {'handled': False}
    use_dot_notation = True


class Activity(Document):
    __collection__ = 'activities'
    structure = {
        'uuid': unicode,
        'subscriber': unicode,
        'type': unicode,
        'text': unicode,
        'creation': datetime,
        'data': dict,
    }
    required_fields = ['uuid', 'subscriber', 'type', 'text', 'creation', 'data']
    default_values = {'creation': datetime.utcnow}
    use_dot_notation = True


class Subscriber(Document):
    __collection__ = 'subscribers'
    structure = {
        'uuid': unicode,
        'device': unicode,
        'timezone': unicode,
        'notifications_enabled': bool,
        'favorites': list,
    }
    required_fields = ['uuid', 'device', 'notifications_enabled']
    default_values = {'notifications_enabled': False}
    use_dot_notation = True

    def followed_bills(self):
        return [f[2:] for f in self.favorites if f.startswith('b/')]

    def followed_committees(self):
        return [f[2:] for f in self.favorites if f.startswith('c/')]

    def followed_legislators(self):
        return [f[2:] for f in self.favorites if f.startswith('l/')]
