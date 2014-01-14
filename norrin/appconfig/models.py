import datetime
import uuid

import pytz
from django.db import models
from jsonfield import JSONField


def generate_key():
    return uuid.uuid4().hex[:12]


def utcnow():
    return datetime.datetime.now(tz=pytz.utc)


class Client(models.Model):
    key = models.CharField(max_length=32, default=generate_key)
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Configuration(models.Model):
    key = models.CharField(max_length=32, default=generate_key)
    description = models.TextField()
    payload = JSONField()
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(default=utcnow)

    class Meta:
        ordering = ('key',)

    def __unicode__(self):
        return self.key


class Load(models.Model):
    configuration = models.ForeignKey(Configuration)
    client = models.ForeignKey(Client, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=utcnow)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        if self.client:
            return u"%s:%s %s" % (self.configuration, self.client, self.timestamp.isoformat())
        return u"%s %s" % (self.configuration, self.timestamp.isoformat())
