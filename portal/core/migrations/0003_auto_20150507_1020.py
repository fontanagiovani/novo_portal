# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150413_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destino',
            name='caminho',
            field=models.CharField(help_text='Utilize o caminho app/template - Templates dispon\xedveis:<br>core/portal.html<br>core/portal_secundario.html<br>core/blog.html<br>core/blog_slider.html<br>core/pagina.html<br><br>Em caso de redirect use a url completa - Ex.: http://www.ifmt.edu.br', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='destino',
            name='tipo',
            field=models.CharField(max_length=100, choices=[(b'PORTAL', 'PORTAL'), (b'PORTAL_SECUNDARIO', 'PORTAL SECUND\xc1RIO'), (b'BLOG', 'BLOG'), (b'BLOG_SLIDER', 'BLOG SLIDER'), (b'PAGINA', 'P\xc1GINA INDIVIDUAL'), (b'REDIRECT', 'REDIRECIONAMENTO')]),
            preserve_default=True,
        ),
    ]
