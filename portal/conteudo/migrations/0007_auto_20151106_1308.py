# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0006_auto_20151104_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemgaleria',
            name='imagem',
            field=filer.fields.image.FilerImageField(related_name='imagem_galeria', to='filer.Image'),
        ),
        migrations.AlterField(
            model_name='licitacao',
            name='email_contato',
            field=models.EmailField(max_length=254, verbose_name='Email para contato'),
        ),
    ]
