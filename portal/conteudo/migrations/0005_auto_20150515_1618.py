# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0004_auto_20150507_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=embed_video.fields.EmbedVideoField(help_text='Utilize uma URL de v\xeddeo do YouTube', verbose_name='URL do v\xeddeo'),
            preserve_default=True,
        ),
    ]
