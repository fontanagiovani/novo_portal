# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=1, max_length=2, choices=[(b'1', b'Destaque'), (b'2', b'Link de acesso'), (b'3', b'Governamental'), (b'4', b'Hotsite')])),
                ('titulo', models.CharField(default=b'', max_length=250, verbose_name='T\xedtulo')),
                ('data_publicacao', models.DateTimeField(verbose_name='Data de publica\xe7\xe3o')),
                ('url', models.URLField(default=b'http://', help_text='Insira o endere\xe7o completo (com http://). Ex.: http://www.ifmt.edu.br/', verbose_name='URL')),
                ('publicado', models.BooleanField(default=True, verbose_name='Publicar')),
                ('arquivo', filer.fields.image.FilerImageField(related_name='banners', default=None, verbose_name='Imagem', to='filer.Image')),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='Sites para publica\xe7\xe3o')),
            ],
            options={
                'ordering': ('-data_publicacao', '-id'),
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
            bases=(models.Model,),
        ),
    ]
