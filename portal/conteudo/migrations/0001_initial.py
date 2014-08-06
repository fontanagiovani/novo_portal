# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conteudo'
        db.create_table(u'conteudo_conteudo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campus_origem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Campus'])),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('texto', self.gf('django.db.models.fields.TextField')()),
            ('data_publicacao', self.gf('django.db.models.fields.DateTimeField')()),
            ('fonte', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'conteudo', ['Conteudo'])

        # Adding M2M table for field galerias on 'Conteudo'
        m2m_table_name = db.shorten_name(u'conteudo_conteudo_galerias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conteudo', models.ForeignKey(orm[u'conteudo.conteudo'], null=False)),
            ('galeria', models.ForeignKey(orm[u'conteudo.galeria'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conteudo_id', 'galeria_id'])

        # Adding M2M table for field videos on 'Conteudo'
        m2m_table_name = db.shorten_name(u'conteudo_conteudo_videos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conteudo', models.ForeignKey(orm[u'conteudo.conteudo'], null=False)),
            ('video', models.ForeignKey(orm[u'conteudo.video'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conteudo_id', 'video_id'])

        # Adding model 'Noticia'
        db.create_table(u'conteudo_noticia', (
            (u'conteudo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conteudo.Conteudo'], unique=True, primary_key=True)),
            ('destaque', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('prioridade_destaque', self.gf('django.db.models.fields.CharField')(default='6', max_length=1)),
        ))
        db.send_create_signal(u'conteudo', ['Noticia'])

        # Adding model 'Anexo'
        db.create_table(u'conteudo_anexo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')()),
            ('arquivo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='anexos_noticia', to=orm['filer.File'])),
            ('conteudo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conteudo.Conteudo'])),
        ))
        db.send_create_signal(u'conteudo', ['Anexo'])

        # Adding model 'Pagina'
        db.create_table(u'conteudo_pagina', (
            (u'conteudo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conteudo.Conteudo'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'conteudo', ['Pagina'])

        # Adding model 'Evento'
        db.create_table(u'conteudo_evento', (
            (u'conteudo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conteudo.Conteudo'], unique=True, primary_key=True)),
            ('local', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('data_inicio', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_fim', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'conteudo', ['Evento'])

        # Adding model 'Video'
        db.create_table(u'conteudo_video', (
            (u'conteudo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conteudo.Conteudo'], unique=True, primary_key=True)),
            ('id_video_youtube', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'conteudo', ['Video'])

        # Adding model 'Galeria'
        db.create_table(u'conteudo_galeria', (
            (u'conteudo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conteudo.Conteudo'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'conteudo', ['Galeria'])

        # Adding model 'ImagemGaleria'
        db.create_table(u'conteudo_imagemgaleria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('imagem', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Imagem Galeria', to=orm['filer.Image'])),
            ('galeria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conteudo.Galeria'])),
        ))
        db.send_create_signal(u'conteudo', ['ImagemGaleria'])


    def backwards(self, orm):
        # Deleting model 'Conteudo'
        db.delete_table(u'conteudo_conteudo')

        # Removing M2M table for field galerias on 'Conteudo'
        db.delete_table(db.shorten_name(u'conteudo_conteudo_galerias'))

        # Removing M2M table for field videos on 'Conteudo'
        db.delete_table(db.shorten_name(u'conteudo_conteudo_videos'))

        # Deleting model 'Noticia'
        db.delete_table(u'conteudo_noticia')

        # Deleting model 'Anexo'
        db.delete_table(u'conteudo_anexo')

        # Deleting model 'Pagina'
        db.delete_table(u'conteudo_pagina')

        # Deleting model 'Evento'
        db.delete_table(u'conteudo_evento')

        # Deleting model 'Video'
        db.delete_table(u'conteudo_video')

        # Deleting model 'Galeria'
        db.delete_table(u'conteudo_galeria')

        # Deleting model 'ImagemGaleria'
        db.delete_table(u'conteudo_imagemgaleria')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'conteudo.anexo': {
            'Meta': {'object_name': 'Anexo'},
            'arquivo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anexos_noticia'", 'to': u"orm['filer.File']"}),
            'conteudo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conteudo.Conteudo']"}),
            'descricao': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'conteudo.conteudo': {
            'Meta': {'ordering': "('-data_publicacao', '-id')", 'object_name': 'Conteudo'},
            'campus_origem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Campus']"}),
            'data_publicacao': ('django.db.models.fields.DateTimeField', [], {}),
            'fonte': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'galerias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['conteudo.Galeria']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'texto': ('django.db.models.fields.TextField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['conteudo.Video']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'conteudo.evento': {
            'Meta': {'ordering': "('-data_publicacao', '-id')", 'object_name': 'Evento', '_ormbases': [u'conteudo.Conteudo']},
            u'conteudo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conteudo.Conteudo']", 'unique': 'True', 'primary_key': 'True'}),
            'data_fim': ('django.db.models.fields.DateTimeField', [], {}),
            'data_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            'local': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'conteudo.galeria': {
            'Meta': {'ordering': "('-data_publicacao', '-id')", 'object_name': 'Galeria', '_ormbases': [u'conteudo.Conteudo']},
            u'conteudo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conteudo.Conteudo']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'conteudo.imagemgaleria': {
            'Meta': {'object_name': 'ImagemGaleria'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'galeria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conteudo.Galeria']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Imagem Galeria'", 'to': "orm['filer.Image']"})
        },
        u'conteudo.noticia': {
            'Meta': {'ordering': "('-data_publicacao', '-id')", 'object_name': 'Noticia', '_ormbases': [u'conteudo.Conteudo']},
            u'conteudo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conteudo.Conteudo']", 'unique': 'True', 'primary_key': 'True'}),
            'destaque': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prioridade_destaque': ('django.db.models.fields.CharField', [], {'default': "'6'", 'max_length': '1'})
        },
        u'conteudo.pagina': {
            'Meta': {'ordering': "('-data_publicacao', '-id')", 'object_name': 'Pagina', '_ormbases': [u'conteudo.Conteudo']},
            u'conteudo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conteudo.Conteudo']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'conteudo.video': {
            'Meta': {'ordering': "('-data_publicacao', '-id')", 'object_name': 'Video', '_ormbases': [u'conteudo.Conteudo']},
            u'conteudo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conteudo.Conteudo']", 'unique': 'True', 'primary_key': 'True'}),
            'id_video_youtube': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
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
        u'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'all_files'", 'null': 'True', 'to': u"orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'owned_files'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_filer.file_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'filer.folder': {
            'Meta': {'ordering': "(u'name',)", 'unique_together': "((u'parent', u'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'filer_owned_folders'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['filer.Folder']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image', '_ormbases': [u'filer.File']},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['conteudo']