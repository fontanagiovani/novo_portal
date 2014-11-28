# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50, verbose_name='Nome do C\xe2mpus')),
            ],
            options={
                'verbose_name': 'Campus',
                'verbose_name_plural': 'Campi',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContadorVisitas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('modificado_em', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=2000)),
                ('contagem', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-contagem', '-criado_em', '-modificado_em'),
                'get_latest_by': 'criado_em',
                'verbose_name': 'Contador de visitas',
                'verbose_name_plural': 'Contador de visitas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=100, choices=[(b'PORTAL', 'PORTAL'), (b'PORTAL_SECUNDARIO', 'PORTAL SECUND\xc1RIO'), (b'BLOG', 'BLOG'), (b'BLOG_SLIDER', 'BLOG SLIDER'), (b'REDIRECT', 'REDIRECIONAMENTO')])),
                ('caminho', models.CharField(help_text='Utilize o caminho app/template - Templates dispon\xedveis:<br>core/portal.html<br>core/portal_secundario.html<br>core/blog.html<br>core/blog_slider.html<br>core/banners.html<br><br>Em caso de redirect use a url completa - Ex.: http://www.ifmt.edu.br', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Selecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=250)),
                ('status', models.CharField(max_length=3, choices=[(b'ABT', b'Aberto'), (b'AND', b'Em Andamento'), (b'FNZ', b'Finalizado')])),
                ('data_abertura_edital', models.DateTimeField(verbose_name='Data de Abertura do Edital')),
                ('data_abertura_inscricoes', models.DateTimeField(verbose_name='Data de Abertura de Inscri\xe7\xf5es')),
                ('data_encerramento_inscricoes', models.DateTimeField(verbose_name='Data de Fechamento das Incri\xe7\xf5es')),
                ('data_publicacao', models.DateTimeField(verbose_name='Data de publica\xe7\xe3o')),
            ],
            options={
                'ordering': ('titulo', 'status', 'data_abertura_edital'),
                'verbose_name': 'Sele\xe7\xe3o',
                'verbose_name_plural': 'Sele\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteDetalhe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hotsite', models.BooleanField(default=False)),
                ('modal', models.TextField(null=True, blank=True)),
                ('social', models.TextField(null=True, blank=True)),
                ('links_uteis', models.TextField(null=True, blank=True)),
                ('mapa_site', models.TextField(null=True, blank=True)),
                ('endereco', models.TextField(null=True, blank=True)),
                ('campus', models.ForeignKey(help_text='C\xe2mpus ou local que este site est\xe1 relacionado', to='core.Campus')),
                ('destino', models.ForeignKey(help_text='Destino da p\xe1gina inicial', to='core.Destino')),
                ('logo', filer.fields.image.FilerImageField(to='filer.Image')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoSelecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Identificador')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='pai', verbose_name=b'Tipo pai', blank=True, to='core.TipoSelecao', null=True)),
            ],
            options={
                'ordering': ('titulo',),
                'verbose_name': 'Tipo de sele\xe7\xe3o',
                'verbose_name_plural': 'Tipos de sele\xe7\xe3o',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='selecao',
            name='tipo',
            field=mptt.fields.TreeForeignKey(to='core.TipoSelecao'),
            preserve_default=True,
        ),
    ]
