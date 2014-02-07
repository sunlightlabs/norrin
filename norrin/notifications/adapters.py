import logging
import uuid

import urbanairship as ua

logger = logging.getLogger('norrin.notifications.adapters')


class UrbanAirshipAdapter(object):

    def __init__(self, airship):
        self.airship = airship

    def push(self, notification):


        push = self.airship.create_push()
        push.audience = self.make_tags(notification.tags)
        push.notification = ua.notification(ios=ua.ios(alert=notification.message, extra=notification.context))
        push.device_types = ua.device_types('ios')

        if notification.scheduled_for:
            schedule = self.airship.create_scheduled_push()
            schedule.push = push
            schedule.name = notification.type
            schedule.schedule = ua.scheduled_time(notification.scheduled_for)
            schedule.send()
        else:
            logger.info("Pushing to Urban Airship")
            push.send()

    def make_tags(self, val):
        if isinstance(val, list):
            return ua.and_(*[self.make_tags(v) for v in val])
        elif isinstance(val, dict):
            if 'or' in val:
                return ua.or_(*[self.make_tags(v) for v in val['or']])
        else:
            return ua.tag(val)



class ConsoleAdapter(object):

    def push(self, notification):
        print "Notification: %s" % notification.message
        print "        tags: %s" % ", ".join(notification.tags)
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
        obj.id = unicode(uuid.uuid4().hex)
        obj.type = unicode(notification.type)
        obj.message = unicode(notification.message)
        obj.payload = {
            'tags': notification.tags,
            'context': notification.context,
            'scheduled_for': notification.scheduled_for,
        }
        obj.save()


class EmailAdapter(object):

    def __init__(self, recipients):
        pass

    def push(self, notification):
        pass
