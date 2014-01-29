from django.conf.urls import patterns, url
from norrin.notifications.views import StatusView

urlpatterns = patterns('',
    url(r'^status/$', StatusView.as_view()),
)
