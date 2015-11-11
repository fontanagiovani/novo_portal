# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0003_banner_nova_janela'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(help_text='Para urls externas utilize o endere\xe7o completo. Ex.:<br>http://www.ifmt.edu.br/<br><br>Para p\xe1ginas internas utilize a url gerada na \xe1rea de conte\xfado/p\xe1gina. Ex.:<br>/conteudo/pagina/inscricoes-workif/', max_length=250),
        ),
    ]
