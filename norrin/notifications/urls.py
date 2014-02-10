from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from norrin.notifications.views import NotificationView, NotificationListView

urlpatterns = patterns('',
    url(r'^(?P<notification_id>\w{8,32})/$', login_required(NotificationView.as_view()), name='notification_detail'),
    url(r'^$', login_required(NotificationListView.as_view()), name='notification_list'),
)
