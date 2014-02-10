from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from norrin.appconfig.views import ConfigurationView

urlpatterns = patterns('',
    url(r'^(?P<key>\w{12})(?P<client_key>\w{12})(?:\.(?P<format>plist|json))?$', ConfigurationView.as_view()),
    url(r'^(?P<key>\w{12})(?:\.(?P<format>plist|json))?$', ConfigurationView.as_view(), {'client_key': None}),
    url(r'^$', TemplateView.as_view(template_name='appconfig/index.html')),
)
