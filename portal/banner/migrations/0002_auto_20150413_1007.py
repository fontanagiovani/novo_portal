# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.URLField(help_text='Insira o endere\xe7o completo (com http://). Ex.: http://www.ifmt.edu.br/', verbose_name='URL'),
            preserve_default=True,
        ),
    ]
