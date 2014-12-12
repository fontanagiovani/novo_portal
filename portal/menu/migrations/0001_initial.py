# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('url', models.CharField(help_text='Para urls externas utilize o endere\xe7o completo. Ex.:<br>http://www.ifmt.edu.br/<br><br>Para p\xe1ginas internas utilize a url gerada na \xe1rea de conte\xfado/p\xe1gina. Ex.:<br>/conteudo/pagina/inscricoes-workif/', max_length=250, null=True, blank=True)),
                ('ordem', models.PositiveIntegerField()),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='pai', verbose_name='Menu pai', blank=True, to='menu.Menu', null=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'ordering': ('ordem',),
            },
            bases=(models.Model,),
        ),
    ]
