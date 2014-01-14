# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'appconfig_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(default='5b5a2fc6e1f4', max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, blank=True)),
        ))
        db.send_create_signal(u'appconfig', ['Client'])

        # Adding model 'Configuration'
        db.create_table(u'appconfig_configuration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(default='e43c0c85be3c', max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('payload', self.gf('jsonfield.fields.JSONField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'appconfig', ['Configuration'])

        # Adding model 'Load'
        db.create_table(u'appconfig_load', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('configuration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appconfig.Configuration'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appconfig.Client'], null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'appconfig', ['Load'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'appconfig_client')

        # Deleting model 'Configuration'
        db.delete_table(u'appconfig_configuration')

        # Deleting model 'Load'
        db.delete_table(u'appconfig_load')


    models = {
        u'appconfig.client': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Client'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'9fb046098c22'", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'appconfig.configuration': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Configuration'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'7d1cae36ad3d'", 'max_length': '32'}),
            'payload': ('jsonfield.fields.JSONField', [], {})
        },
        u'appconfig.load': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Load'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appconfig.Client']", 'null': 'True', 'blank': 'True'}),
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appconfig.Configuration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['appconfig']