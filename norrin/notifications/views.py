from django.shortcuts import render
from django.views.generic import View
from mongokit import Connection

from norrin.notifications import config
from norrin.notifications.models import Notification


conn = Connection(config.MONGODB_HOST, config.MONGODB_PORT)
db = conn[config.MONGODB_DATABASE]
if config.MONGODB_USERNAME and config.MONGODB_PASSWORD:
    db.authenticate(config.MONGODB_USERNAME, config.MONGODB_PASSWORD)


class StatusView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'recent_notifications': [n for n in db.notifications.find({}).limit(20).sort("timestamp", -1)],
        }
        return render(request, 'notifications/status.html', context)


class NotificationView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'notification': db.notifications.find_one({'id': kwargs.get('notification_id')})
        }
        return render(request, 'notifications/notification.html', context)
