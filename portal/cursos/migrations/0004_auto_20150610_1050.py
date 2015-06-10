# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_auto_20150608_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupocursos',
            name='nome',
            field=models.CharField(help_text='Ex.: Licenciatura em Matem\xe1tica', unique=True, max_length=80, verbose_name='Nome Gen\xe9rico para Curso'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupocursos',
            name='slug',
            field=models.SlugField(help_text='Texto que identificar\xe1 a URL deste item (n\xe3o deve conter espa\xe7os ou caracteres especiais)', unique=True, max_length=250, verbose_name='Identificador'),
            preserve_default=True,
        ),
    ]
