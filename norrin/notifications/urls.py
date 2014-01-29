from django.conf.urls import patterns, url
from norrin.notifications.views import StatusView, NotificationView

urlpatterns = patterns('',
    url(r'^status/$', StatusView.as_view()),
    url(r'^(?P<notification_id>\w{32})/$', NotificationView.as_view(), name='notification_detail'),
)
