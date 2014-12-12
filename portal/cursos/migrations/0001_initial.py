# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnexoCurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=250, verbose_name='Descri\xe7\xe3o do anexo')),
                ('arquivo', filer.fields.file.FilerFileField(related_name='anexos_curso', to='filer.File')),
            ],
            options={
                'verbose_name': 'Anexo',
                'verbose_name_plural': 'Anexos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='Ex.: Licenciatura em Matem\xe1tica Noturno', max_length=100, verbose_name='Nome do Curso')),
                ('slug', models.SlugField(help_text='Texto que identificar\xe1 a URL deste item (n\xe3o deve conter espa\xe7os ou caracteres especiais)', max_length=250, verbose_name='Identificador')),
                ('turno', models.CharField(max_length=3, verbose_name='Turno do Curso', choices=[(b'MAT', 'Matutino'), (b'VES', 'Vespertino'), (b'NOT', 'Noturno'), (b'INT', 'Integral')])),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email', blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('campus', models.ForeignKey(verbose_name='C\xe2mpus', to='core.Campus')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Formacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100, verbose_name='Nome da Forma\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'Tipo de Forma\xe7\xe3o',
                'verbose_name_plural': 'Tipos de Forma\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoCursos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='Ex.: Licenciatura em Matem\xe1tica', max_length=80, verbose_name='Nome Gen\xe9rico para Curso')),
                ('slug', models.SlugField(help_text='Texto que identificar\xe1 a URL deste item (n\xe3o deve conter espa\xe7os ou caracteres especiais)', max_length=250, verbose_name='Identificador')),
            ],
            options={
                'verbose_name': 'Grupo de Cursos',
                'verbose_name_plural': 'Grupo de Cursos',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='curso',
            name='formacao',
            field=models.ForeignKey(verbose_name='Tipo de Forma\xe7\xe3o', to='cursos.Formacao'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curso',
            name='grupo',
            field=models.ForeignKey(to='cursos.GrupoCursos'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anexocurso',
            name='curso',
            field=models.ForeignKey(verbose_name='Curso', to='cursos.Curso'),
            preserve_default=True,
        ),
    ]
