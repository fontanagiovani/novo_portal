# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0002_auto_20141212_0842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anexolicitacao',
            options={'verbose_name': 'Anexo da licitacao', 'verbose_name_plural': 'Anexos da licitacao'},
        ),
        migrations.AlterModelOptions(
            name='conteudo',
            options={'ordering': ('-data_publicacao', '-id'), 'verbose_name': 'Conteudo', 'verbose_name_plural': 'Conteudos'},
        ),
        migrations.AlterModelOptions(
            name='licitacao',
            options={'verbose_name': 'Licitacao', 'verbose_name_plural': 'Licitacoes'},
        ),
        migrations.AlterModelOptions(
            name='noticia',
            options={'ordering': ('-data_publicacao', '-id'), 'verbose_name': 'Noticia', 'verbose_name_plural': 'Noticias'},
        ),
        migrations.AlterModelOptions(
            name='pagina',
            options={'verbose_name': 'Pagina', 'verbose_name_plural': 'Paginas'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
        migrations.AddField(
            model_name='pagina',
            name='pagina_inicial',
            field=models.BooleanField(default=False, verbose_name='P\xe1gina inicial'),
            preserve_default=True,
        ),
    ]
