# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Configuration.payload'
        db.alter_column(u'appconfig_configuration', 'payload', self.gf('jsonfield.fields.JSONField')(null=True))

    def backwards(self, orm):

        # Changing field 'Configuration.payload'
        db.alter_column(u'appconfig_configuration', 'payload', self.gf('jsonfield.fields.JSONField')(default=None))

    models = {
        u'appconfig.client': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Client'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'09f3e14155bc'", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'appconfig.configuration': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Configuration'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 24, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'adc96b76d246'", 'max_length': '32'}),
            'payload': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'})
        },
        u'appconfig.load': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Load'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appconfig.Client']", 'null': 'True', 'blank': 'True'}),
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appconfig.Configuration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 24, 0, 0)'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['appconfig']