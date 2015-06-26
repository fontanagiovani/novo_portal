# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_auto_20150413_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='nova_janela',
            field=models.BooleanField(default=False, verbose_name='Abrir em uma nova janela?'),
            preserve_default=True,
        ),
    ]
