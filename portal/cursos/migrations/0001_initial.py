# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Formacao'
        db.create_table(u'cursos_formacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'cursos', ['Formacao'])

        # Adding model 'GrupoCursos'
        db.create_table(u'cursos_grupocursos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('descricao', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cursos', ['GrupoCursos'])

        # Adding model 'Curso'
        db.create_table(u'cursos_curso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('formacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cursos.Formacao'])),
            ('campus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Campus'])),
            ('turno', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cursos.GrupoCursos'])),
        ))
        db.send_create_signal(u'cursos', ['Curso'])


    def backwards(self, orm):
        # Deleting model 'Formacao'
        db.delete_table(u'cursos_formacao')

        # Deleting model 'GrupoCursos'
        db.delete_table(u'cursos_grupocursos')

        # Deleting model 'Curso'
        db.delete_table(u'cursos_curso')


    models = {
        u'core.campus': {
            'Meta': {'object_name': 'Campus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'pai'", 'null': 'True', 'to': u"orm['core.Campus']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cursos.curso': {
            'Meta': {'object_name': 'Curso'},
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Campus']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'formacao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cursos.Formacao']"}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cursos.GrupoCursos']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'turno': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'cursos.formacao': {
            'Meta': {'object_name': 'Formacao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cursos.grupocursos': {
            'Meta': {'object_name': 'GrupoCursos'},
            'descricao': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['cursos']