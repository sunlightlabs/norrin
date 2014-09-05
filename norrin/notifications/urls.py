from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from norrin.notifications.views import NotificationView, NotificationListView, PowerView, SendView, RSSView

urlpatterns = patterns('',
    url(r'^(?P<notification_id>\w{8,32})/$', login_required(NotificationView.as_view()), name='notification_detail'),
    url(r'^(?P<notification_id>\w{8,32})/send/$', csrf_exempt(login_required(SendView.as_view())), name='notification_send'),
    url(r'^power/$', login_required(PowerView.as_view()), name='notification_power'),
    url(r'^rss/$', RSSView.as_view(), name='notification_rss'),
    url(r'^$', login_required(NotificationListView.as_view()), name='notification_list'),
)
