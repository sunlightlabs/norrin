from django.conf.urls import patterns, include, url
from norrin.appconfig.views import ConfigurationView

urlpatterns = patterns('',
    url(r'^(?P<key>\w{12})(?P<client_key>\w{12})(?:\.(?P<format>plist|json))?$', ConfigurationView.as_view()),
    url(r'^(?P<key>\w{12})(?:\.(?P<format>plist|json))?$', ConfigurationView.as_view(), {'client_key': None}),
)
