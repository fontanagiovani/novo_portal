# -*- coding: utf-8 -*-
# https://docs.djangoproject.com/en/1.7/ref/migration-operations/#runpython
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    GrupoCursos = apps.get_model("cursos", "GrupoCursos")
    Curso = apps.get_model("cursos", "Curso")
    db_alias = schema_editor.connection.alias
    grupos = Curso.objects.using(db_alias).select_related('GrupoCursos').values('grupo__slug').distinct()
    for grupo in grupos:
        slug_grupo = grupo.get('grupo__slug')
        grupos_semelhantes = GrupoCursos.objects.using(db_alias).filter(slug=slug_grupo)
        if grupos_semelhantes.count() >1:
            grupo_curso = grupos_semelhantes[0]
            for g in grupos_semelhantes:
                for curso in g.curso_set.all():
                    curso.grupo = grupo_curso
                    curso.save()
                if grupo_curso.pk != g.pk:
                    g.delete()

    # import ipdb
    # ipdb.set_trace()

class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_auto_20150413_1007'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
        migrations.AlterField(
            model_name='grupocursos',
            name='nome',
            field=models.CharField(help_text='Ex.: Licenciatura em Matem\xe1tica', unique=True, max_length=80, verbose_name='Nome Gen\xe9rico para Curso'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grupocursos',
            name='slug',
            field=models.SlugField(help_text='Texto que identificar\xe1 a URL deste item (n\xe3o deve conter espa\xe7os ou caracteres especiais)', unique=True, max_length=250, verbose_name='Identificador'),
            preserve_default=True,
        ),
    ]
