# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Midia'
        db.delete_table(u'core_midia')

        # Deleting model 'Conteudo'
        db.delete_table(u'core_conteudo')


    def backwards(self, orm):
        # Adding model 'Midia'
        db.create_table(u'core_midia', (
            ('conteudo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conteudo'])),
            ('arquivo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='arquivos_midia', to=orm['filer.File'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Midia'])

        # Adding model 'Conteudo'
        db.create_table(u'core_conteudo', (
            ('destaque', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('texto', self.gf('django.db.models.fields.TextField')()),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='NOTICIA', max_length=250)),
            ('campus_origem', self.gf('django.db.models.fields.CharField')(default='RTR', max_length=250)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=250)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_publicacao', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['Conteudo'])


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
        }
    }

    complete_apps = ['core']