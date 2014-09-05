import math

import urbanairship as ua
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from mongokit import Connection

from norrin import config
from norrin import settings
from norrin.notifications.adapters import LoggingAdapter, UrbanAirshipAdapter
from norrin.notifications.models import connection, Notification
from norrin.notifications.services import Service, adapters

db = connection[settings.MONGODB_DATABASE]

adapters.register(UrbanAirshipAdapter(ua.Airship(settings.UA_KEY, settings.UA_MASTER)))
adapters.register(LoggingAdapter)


class StatusView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'recent_notifications': [n for n in db.Notification.find({}).limit(5).sort("timestamp", -1)]
        }
        return render(request, 'notifications/status.html', context)


class NotificationView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'notification': db.Notification.find_one({'id': kwargs.get('notification_id')})
        }
        return render(request, 'notifications/notification.html', context)


class NotificationListView(View):

    per_page = 20

    def get(self, request, *args, **kwargs):

        page = int(request.GET.get('page') or 1)
        offset = (page - 1) * self.per_page

        qs = db.Notification.find({})
        notifications = qs.sort('timestamp', -1).limit(self.per_page).skip(offset)

        total_count = qs.count()
        total_pages = int(math.ceil(total_count / float(self.per_page)))

        context = {
            'notifications': [n for n in qs],
            'pages': {
                'current': page,
                'total': total_pages,
                'next_page': page + 1 if page < total_pages else None,
                'previous_page': page - 1 if page > 1 else None,
            }
        }

        return render(request, 'notifications/notification_list.html', context)


class PowerView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'notifications/power.html')

    def post(self, request, *args, **kwargs):
        status = request.POST.get('status')
        if status in ('on', 'off'):
            config.set(config.SERVICES_ENABLED, status)
        return HttpResponseRedirect('/notifications/power/')


class SendView(View):

    def post(self, request, *args, **kwargs):
        notification = db.Notification.find_one({'id': kwargs.get('notification_id')})
        # if notification and not notification.sent:
        if notification:
            Service().push_notification(notification)
        return HttpResponse('{}', content_type='application/json')


class RSSView(View):

    def get(self, request, *args, **kwargs):
        notifications = db.Notification.find({}).sort('timestamp', -1).limit(30)
        context = {'notifications': notifications}
        return render(request, 'notifications/feed.rss', context, content_type='application/rss+xml')
