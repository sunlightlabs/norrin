import urbanairship as ua


class UrbanAirshipAdapter(object):

    def __init__(self, airship):
        self.airship = airship

    def push(self, notification):
        push = self.airship.create_push()
        push.audience = ua.tag(notification.tags[0])
        push.notification = ua.ios(alert=notification.message)
        push.device_types = ua.all_
        push.send()


class ConsoleAdapter(object):

    def push(self, notification):
        print "Notification: %s" % notification.message
        print "        tags: %s" % ", ".join(notification.tags)


class EmailAdapter(object):

    def __init__(self, recipients):
        pass

    def push(self, notification):
        pass
