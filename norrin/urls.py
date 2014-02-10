from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from norrin.notifications.views import StatusView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^config/', include('norrin.appconfig.urls')),
    url(r'^notifications/', include('norrin.notifications.urls')),
    url(r'^', include('googleauth.urls')),
    url(r'^$', login_required(StatusView.as_view())),
)
