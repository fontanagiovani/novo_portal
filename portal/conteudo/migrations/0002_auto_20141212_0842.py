# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemgaleria',
            name='descricao',
            field=models.CharField(max_length=250, null=True, verbose_name='Descri\xe7\xe3o', blank=True),
            preserve_default=True,
        ),
    ]
