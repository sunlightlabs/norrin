import logging

import urbanairship as ua


class UrbanAirshipAdapter(object):

    def __init__(self, airship):
        self.airship = airship

    def push(self, notification):

        push = self.airship.create_push()
        push.audience = ua.tag(notification.tags[0])
        push.notification = ua.notification(ios=ua.ios(alert=notification.message, extra=notification.context))
        push.device_types = ua.device_types('ios')

        if notification.scheduled_for:
            schedule = self.airship.create_scheduled_push()
            schedule.push = push
            schedule.name = notification.type
            schedule.schedule = ua.scheduled_time(notification.scheduled_for)
            schedule.send()
        else:
            push.send()


class ConsoleAdapter(object):

    def push(self, notification):
        print "Notification: %s" % notification.message
        print "        tags: %s" % ", ".join(notification.tags)
        if notification.scheduled_for:
            print "   scheduled: %s" % notification.scheduled_for


class LoggingAdapter(object):

    def __init__(self):
        self.logger = logging.getLogger('norrin.notifications.adapters')

    def push(self, notification):
        self.logger.info("Notification:%s tags:%s" % (notification.message, ",".join(notification.tags)))


class MongoDBAdapter(object):

    def __init__(self, db):
        self.db = db

    def push(self, notification):
        pass


class EmailAdapter(object):

    def __init__(self, recipients):
        pass

    def push(self, notification):
        pass
