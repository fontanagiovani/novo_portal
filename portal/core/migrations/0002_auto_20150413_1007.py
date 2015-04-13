# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='selecao',
            options={'ordering': ('titulo', 'status', 'data_abertura_edital'), 'verbose_name': 'Selecao', 'verbose_name_plural': 'Selecoes'},
        ),
        migrations.AlterModelOptions(
            name='tiposelecao',
            options={'ordering': ('titulo',), 'verbose_name': 'Tipo de selecao', 'verbose_name_plural': 'Tipos de selecao'},
        ),
    ]
