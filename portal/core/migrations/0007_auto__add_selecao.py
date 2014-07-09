# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Selecao'
        db.create_table(u'core_selecao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('data_abertura_edital', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_abertura_inscricoes', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_encerramento_inscricoes', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_publicacao', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['Selecao'])


    def backwards(self, orm):
        # Deleting model 'Selecao'
        db.delete_table(u'core_selecao')


    models = {
        u'core.menu': {
            'Meta': {'ordering': "('titulo',)", 'object_name': 'Menu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'pai'", 'null': 'True', 'to': u"orm['core.Menu']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'core.selecao': {
            'Meta': {'ordering': "('titulo', 'status', 'data_abertura_edital')", 'object_name': 'Selecao'},
            'data_abertura_edital': ('django.db.models.fields.DateTimeField', [], {}),
            'data_abertura_inscricoes': ('django.db.models.fields.DateTimeField', [], {}),
            'data_encerramento_inscricoes': ('django.db.models.fields.DateTimeField', [], {}),
            'data_publicacao': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['core']