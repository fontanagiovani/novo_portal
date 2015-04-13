# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacao', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permissao',
            options={'verbose_name': 'Permissao de Publicacao', 'verbose_name_plural': 'Permissoes de Publicacao'},
        ),
    ]
