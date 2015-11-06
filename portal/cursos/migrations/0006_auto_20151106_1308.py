# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0005_auto_20150610_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
    ]
