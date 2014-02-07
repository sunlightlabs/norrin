from django.conf.urls import patterns, url
from norrin.notifications.views import StatusView, NotificationView, NotificationListView

urlpatterns = patterns('',
    url(r'^status/$', StatusView.as_view()),
    url(r'^all/$', NotificationListView.as_view()),
    url(r'^(?P<notification_id>\w{8,32})/$', NotificationView.as_view(), name='notification_detail'),
)
