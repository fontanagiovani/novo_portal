# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0003_auto_20150413_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagina',
            name='pagina_inicial',
            field=models.BooleanField(default=False, help_text='Esse campo \xe9 utilizado para sites que possuem uma p\xe1gina simples como p\xe1gina inicial. Para definir esta p\xe1gina como sendo a p\xe1gina inicial marque esta op\xe7\xe3o.', verbose_name='P\xe1gina inicial'),
            preserve_default=True,
        ),
    ]
