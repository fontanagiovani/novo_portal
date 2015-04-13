# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formacao',
            options={'verbose_name': 'Tipo de Formacao', 'verbose_name_plural': 'Tipos de Formacoes'},
        ),
    ]
