# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Selecao.slug'
        db.delete_column(u'core_selecao', 'slug')


    def backwards(self, orm):
        # Adding field 'Selecao.slug'
        db.add_column(u'core_selecao', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=100, unique=True, blank=True),
                      keep_default=False)


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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['core']