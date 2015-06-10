# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0004_auto_20150610_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='slug',
            field=models.SlugField(help_text='Texto que identificar\xe1 a URL deste item (n\xe3o deve conter espa\xe7os ou caracteres especiais)', unique=True, max_length=250, verbose_name='Identificador'),
            preserve_default=True,
        ),
    ]
