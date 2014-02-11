import os
from urlparse import urlparse

import redis
from norrin import settings

SERVICES_ENABLED = 'notifications.services.enabled'


url = urlparse(settings.REDISCLOUD_URL)
conn = redis.Redis(host=url.hostname, port=url.port, password=url.password)

def get(k, default=None):
    v = conn.get(k)
    print "GET %s:%s" % (k, v)
    return default if v is None else v

def set(k, v):
    resp = conn.set(k, v)
    print "SET %s:%s = %s" % (k, v, resp)
