# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='Sites Permitidos')),
                ('user', models.OneToOneField(verbose_name='Usu\xe1rio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Permiss\xe3o de Publicac\xe3o',
                'verbose_name_plural': 'Permiss\xf5es de Publica\xe7\xe3o',
            },
            bases=(models.Model,),
        ),
    ]
