# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150507_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitedetalhe',
            name='disqus_shortname',
            field=models.CharField(help_text='ShortName do site no servi\xe7o de coment\xe1rios DISQUS', max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
