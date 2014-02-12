import logging

import urbanairship as ua
from norrin import config

logger = logging.getLogger('norrin.notifications.adapters')


class UrbanAirshipAdapter(object):

    def __init__(self, airship):
        self.airship = airship

    def push(self, notification):

        if not config.get(config.SERVICES_ENABLED, 'off') == 'on':
            logger.info('notifications disabled: %s marked as pending' % notification.id)
            return

        push = self.airship.create_push()
        push.audience = self.make_tags(notification.tags)
        push.notification = ua.notification(ios=ua.ios(alert=notification.message, extra=notification.payload))
        push.device_types = ua.device_types('ios')

        if notification.scheduled_for:
            schedule = self.airship.create_scheduled_push()
            schedule.push = push
            schedule.name = notification.type
            schedule.schedule = ua.scheduled_time(notification.scheduled_for)
            resp = schedule.send()
        else:
            logger.info("Pushing to Urban Airship")
            resp = push.send()

        notification.meta['ua_response'] = resp.payload
        notification.sent = True

    def make_tags(self, val):
        if isinstance(val, list):
            return ua.and_(*[self.make_tags(v) for v in val])
        elif isinstance(val, dict):
            if 'or' in val:
                return ua.or_(*[self.make_tags(v) for v in val['or']])
            elif 'and' in val:
                return ua.and_(*[self.make_tags(v) for v in val['and']])
        else:
            return ua.tag(val)



class ConsoleAdapter(object):

    def push(self, notification):
        print "Notification: %s" % notification.message
        print "        tags: %s" % notification.tags
        if notification.scheduled_for:
            print "   scheduled: %s" % notification.scheduled_for


class LoggingAdapter(object):

    def push(self, notification):
        logger.info("Notification:%s tags:%s" % (notification.message, ",".join(notification.tags)))


class MongoDBAdapter(object):

    def __init__(self, db):
        self.db = db

    def push(self, notification):
        obj = self.db.Notification()
        obj.id = unicode(notification.id)
        obj.type = unicode(notification.type)
        obj.message = unicode(notification.message)
        obj.payload = {
            'tags': notification.tags,
            'payload': notification.payload,
            'scheduled_for': notification.scheduled_for,
        }
        obj.save()


class EmailAdapter(object):

    def __init__(self, recipients):
        pass

    def push(self, notification):
        pass
