import json
import plistlib

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View

from norrin.appconfig.models import Configuration, Client, Load

EXTENSIONS = {
    'json': 'application/json',
    'plist': 'application/x-plist',
}
MIMETYPES = dict((v, k) for k, v in EXTENSIONS.items())


class JSONResponse(HttpResponse):
    def __init__(self, payload):
        content = json.dumps(payload)
        super(JSONResponse, self).__init__(content, content_type=EXTENSIONS['json'])


class PlistResponse(HttpResponse):
    def __init__(self, payload):
        content = plistlib.writePlistToString(payload or {})
        super(PlistResponse, self).__init__(content, content_type=EXTENSIONS['plist'])


class ConfigurationView(View):

    def get(self, request, *args, **kwargs):

        # get format from extension or HTTP Accept header

        format = kwargs.get('format')

        if format and format not in EXTENSIONS:
            raise Http404

        if not format:
            accept = request.META.get('HTTP_ACCEPT', '')
            accept = [a.split(';', 1)[0] for a in accept.split(',')]
            accept = [a for a in accept if a in MIMETYPES]
            if not accept:
                raise Http404
            format = MIMETYPES[accept[0]]

        config = get_object_or_404(Configuration, key=kwargs.get('key'))
        payload = config.payload if config.enabled else {}

        # record configuration loading

        client = None
        client_key = kwargs.get('client_key')
        if client_key:
            try:
                client = Client.objects.get(key=client_key)
            except Client.DoesNotExist:
                pass

        if client:
            ua = request.META.get('HTTP_USER_AGENT', '')
            Load.objects.create(configuration=config, client=client, user_agent=ua)

        # return the response

        return PlistResponse(payload) if format == 'plist' else JSONResponse(payload)
