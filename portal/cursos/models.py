# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField


# class Campus(models.Model):
#     nome = models.CharField(max_length=50, verbose_name=u'Nome do Campus')
#
#     class Meta:
#         verbose_name = u'Campus'
#         verbose_name_plural = u'Campi'
#
#     def __unicode__(self):
#         return self.nome


class Formacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name=u'Nome da Formação')

    class Meta:
        verbose_name = _(u'Tipo de Formacao')
        verbose_name_plural = _(u'Tipos de Formacoes')

    def __unicode__(self):
        return self.nome

    # Doutorado
    # Mestrado
    # Especialização
    # Curso Superior
    # Curso Técnico Integrado ao Ensino Médio
    # Curso Técnico Subsequente
    # Curso Técnico Integrado ao Ensino Médio na modalidade Proeja


class GrupoCursos(models.Model):
    nome = models.CharField(max_length=80, verbose_name=u'Nome Genérico para Curso', unique=True,
                            help_text=u'Ex.: Licenciatura em Matemática')
    slug = models.SlugField(max_length=250, verbose_name=u'Identificador', unique=True,
                            help_text=u'Texto que identificará a URL deste item (não deve conter espaços ou '
                                      u'caracteres especiais)')

    class Meta:
        verbose_name = _(u'Grupo de Cursos')
        verbose_name_plural = _(u'Grupo de Cursos')

    def __unicode__(self):
        return self.nome


class Curso(models.Model):
    TURNO = (
        ('MAT', u'Matutino'),
        ('VES', u'Vespertino'),
        ('NOT', u'Noturno'),
        ('INT', u'Integral'),
    )
    nome = models.CharField(max_length=100, verbose_name=u'Nome do Curso',
                            help_text=u'Ex.: Licenciatura em Matemática Noturno')
    slug = models.SlugField(max_length=250, verbose_name=u'Identificador', unique=True,
                            help_text=u'Texto que identificará a URL deste item (não deve conter espaços ou '
                                      u'caracteres especiais)')
    formacao = models.ForeignKey('Formacao', verbose_name=u'Tipo de Formação')
    campus = models.ForeignKey('core.Campus', verbose_name=u'Câmpus')
    turno = models.CharField(max_length=3, choices=TURNO, verbose_name=u'Turno do Curso')
    descricao = models.TextField(verbose_name=u'Descrição')
    email = models.EmailField(verbose_name=u'email', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    grupo = models.ForeignKey('GrupoCursos')

    class Meta:
        verbose_name = u'Curso'
        verbose_name_plural = u'Cursos'

    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.campus)

    @models.permalink
    def get_absolute_url(self):
        return 'exibecurso', (), {'slug': self.slug}


class AnexoCurso(models.Model):
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição do anexo')
    arquivo = FilerFileField(related_name='anexos_curso')
    curso = models.ForeignKey('Curso', verbose_name=u'Curso')

    class Meta:
        verbose_name = _(u'Anexo')
        verbose_name_plural = _(u'Anexos')

    def __unicode__(self):
        return self.descricao

    # |---------|
    # |Formacao |
    # |---------|
    #     |1
    #     |
    #     |n
    # |------| n     1|-------------|n
    # |Curso |--------| GrupoCursos |
    # |------|        |-------------|
    #     |n
    #     |
    #     |1
    # |------------|
    # |core.Campus |
    # |------------|