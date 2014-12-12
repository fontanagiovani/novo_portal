# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.file
import embed_video.fields
import taggit_autosuggest.managers
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('sites', '0001_initial'),
        ('core', '0001_initial'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anexo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=250, verbose_name='Descri\xe7\xe3o')),
                ('arquivo', filer.fields.file.FilerFileField(related_name='anexos_conteudo', to='filer.File')),
            ],
            options={
                'verbose_name': 'Anexo',
                'verbose_name_plural': 'Anexos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnexoLicitacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=250, verbose_name='Descri\xe7\xe3o')),
                ('arquivo', filer.fields.file.FilerFileField(related_name='anexos_licitacao', to='filer.File')),
            ],
            options={
                'verbose_name': 'Anexo da licita\xe7\xe3o',
                'verbose_name_plural': 'Anexos da licita\xe7\xe3o',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conteudo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=250, verbose_name='T\xedtulo')),
                ('slug', models.SlugField(help_text='Texto que identificar\xe1 a URL deste item (n\xe3o deve conter espa\xe7os ou caracteres especiais)', max_length=250, verbose_name='Identificador')),
                ('texto', models.TextField()),
                ('data_publicacao', models.DateTimeField(verbose_name='Data de publica\xe7\xe3o')),
                ('publicado', models.BooleanField(default=True, verbose_name='Publicar')),
            ],
            options={
                'ordering': ('-data_publicacao', '-id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('conteudo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='conteudo.Conteudo')),
                ('local', models.CharField(max_length=250)),
                ('data_inicio', models.DateTimeField(verbose_name='Data de in\xedcio')),
                ('data_fim', models.DateTimeField(verbose_name='Data de t\xe9rmino')),
            ],
            options={
                'ordering': ('-data_inicio', '-id'),
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
            bases=('conteudo.conteudo',),
        ),
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('conteudo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='conteudo.Conteudo')),
            ],
            options={
                'ordering': ('-data_publicacao', '-id'),
                'verbose_name': 'Galeria',
                'verbose_name_plural': 'Galerias',
            },
            bases=('conteudo.conteudo',),
        ),
        migrations.CreateModel(
            name='ImagemGaleria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=250, verbose_name='Descri\xe7\xe3o')),
                ('galeria', models.ForeignKey(verbose_name='Galeria', to='conteudo.Galeria')),
                ('imagem', filer.fields.image.FilerImageField(related_name='Imagem Galeria', to='filer.Image')),
            ],
            options={
                'verbose_name': 'Anexo de galeria',
                'verbose_name_plural': 'Anexos de galeria',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Licitacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modalidade', models.CharField(max_length=1, verbose_name='Tipo de Modalidade', choices=[(b'1', 'Preg\xe3o'), (b'2', 'Convite'), (b'3', 'Tomada de pre\xe7o'), (b'4', 'Concorr\xeancia')])),
                ('titulo', models.CharField(max_length=100, verbose_name='T\xedtulo')),
                ('data_publicacao', models.DateTimeField(verbose_name='Data de publica\xe7\xe3o')),
                ('data_abertura', models.DateField(verbose_name='Data de abertura')),
                ('pregao_srp', models.BooleanField(default=False, verbose_name='\xc9 um preg\xe3o SRP?')),
                ('validade_ata_srp', models.DateField(null=True, verbose_name='Validade ATA SRP', blank=True)),
                ('possui_contrato', models.BooleanField(default=False, verbose_name='Possui Contrato?')),
                ('vigencia_contrato_inicio', models.DateField(null=True, verbose_name='Data de in\xedcio da vig\xeancia do contrato', blank=True)),
                ('vigencia_contrato_fim', models.DateField(null=True, verbose_name='Data de t\xe9rmino da vig\xeancia do contrato', blank=True)),
                ('encerrado', models.BooleanField(default=False, verbose_name='Processo encerrado?')),
                ('situacao', models.TextField(verbose_name='Situa\xe7\xe3o')),
                ('objeto', models.TextField(verbose_name='Objeto')),
                ('alteracoes', models.TextField(null=True, verbose_name='Altera\xe7\xf5es', blank=True)),
                ('email_contato', models.EmailField(max_length=75, verbose_name='Email para contato')),
                ('publicado', models.BooleanField(default=True, verbose_name='Publicar')),
                ('campus_origem', models.ForeignKey(verbose_name='Origem', to='core.Campus')),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='Sites para publica\xe7\xe3o')),
                ('tags', taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Licita\xe7\xe3o',
                'verbose_name_plural': 'Licita\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('conteudo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='conteudo.Conteudo')),
                ('destaque', models.BooleanField(default=False, verbose_name='Destaque')),
                ('prioridade_destaque', models.CharField(default=b'6', max_length=1, verbose_name='Prioridade de destaque', choices=[(b'1', '1 - Alta'), (b'2', '2 - M\xe9dia-Alta'), (b'3', '3 - M\xe9dia'), (b'4', '4 - Baixa-M\xe9dia'), (b'5', '5 - Baixa'), (b'6', 'Nenhuma')])),
            ],
            options={
                'ordering': ('-data_publicacao', '-id'),
                'verbose_name': 'Not\xedcia',
                'verbose_name_plural': 'Not\xedcias',
            },
            bases=('conteudo.conteudo',),
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('conteudo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='conteudo.Conteudo')),
            ],
            options={
                'verbose_name': 'P\xe1gina',
                'verbose_name_plural': 'P\xe1ginas',
            },
            bases=('conteudo.conteudo',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('conteudo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='conteudo.Conteudo')),
                ('url', embed_video.fields.EmbedVideoField()),
            ],
            options={
                'verbose_name': 'V\xeddeo',
                'verbose_name_plural': 'V\xeddeos',
            },
            bases=('conteudo.conteudo',),
        ),
        migrations.AddField(
            model_name='conteudo',
            name='campus_origem',
            field=models.ForeignKey(verbose_name='Origem', to='core.Campus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conteudo',
            name='galerias',
            field=models.ManyToManyField(to='conteudo.Galeria', verbose_name='Galerias Relacionadas', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conteudo',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', verbose_name='Site(s)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conteudo',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conteudo',
            name='videos',
            field=models.ManyToManyField(to='conteudo.Video', verbose_name='Videos Relacionadas', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anexolicitacao',
            name='licitacao',
            field=models.ForeignKey(verbose_name='Licita\xe7\xe3o', to='conteudo.Licitacao'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anexo',
            name='conteudo',
            field=models.ForeignKey(verbose_name='conteudo', to='conteudo.Conteudo'),
            preserve_default=True,
        ),
    ]
