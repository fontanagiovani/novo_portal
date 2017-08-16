# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(help_text='No m\xe1ximo 250 caracteres', max_length=250, verbose_name='Descri\xe7\xe3o do compromisso')),
                ('inicio', models.DateTimeField(verbose_name='data e hora de in\xedcio do compromisso')),
                ('fim', models.DateTimeField(verbose_name='data e hora do fim do compromisso')),
                ('local', models.CharField(help_text='No m\xe1ximo 100 caracteres', max_length=100, verbose_name='Local do compromisso')),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
                ('data_ultima_modificacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Compromisso',
                'verbose_name_plural': 'Compromissos',
            },
        ),
    ]
