# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Campus(models.Model):
    nome = models.CharField(max_length=50, verbose_name=u'Nome do Campus')

    class Meta:
        verbose_name = u'Campus'
        verbose_name_plural = u'Campi'

    def __unicode__(self):
        return self.nome


class Formacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name=u'Nome da Formação')

    class Meta:
        verbose_name = u'Tipo de Formação'
        verbose_name_plural = u'Tipos de Formações'

    def __unicode__(self):
        return self.nome

    # Doutorado
    # Mestrado
    # Especialização
    # Curso Superior
    # Curso Técnico Integrado ao Ensino Médio
    # Curso Técnico Subsequente
    # Curso Técnico Integrado ao Ensino Médio na modalidade Proeja


class Grupo_Cursos(models.Model):
    nome = models.CharField(max_length=80, verbose_name=u'Nome Genérico para Curso', help_text=u'Ex.: Licenciatura em Matemática')
    descricao = models.TextField(verbose_name=u'Descrição sobre o curso')

    class Meta:
        verbose_name = u'Grupo de Cursos'
        verbose_name_plural = u'Grupo de Cursos'

    def __unicode__(self):
        return self.nome


class Curso(models.Model):
    TURNO = (
        ('MAT', u'Matutino'),
        ('VES', u'Vespertino'),
        ('NOT', u'Noturno'),
        ('INT', u'Integral'),
    )
    nome = models.CharField(max_length=100, verbose_name=u'Nome do Curso', help_text=u'Ex.: Licenciatura em Matemática Noturno')
    formacao = models.ForeignKey(Formacao, verbose_name=u'Tipo de Formação')
    campus = models.ForeignKey(Campus, verbose_name=u'Campus')
    turno = models.CharField(max_length=3, choices=TURNO, verbose_name=u'Turno do Curso')
    email = models.EmailField(verbose_name=u'email')
    url = models.URLField()
    grupo = models.ForeignKey(Grupo_Cursos)

    class Meta:
        verbose_name = u'Curso'
        verbose_name_plural = u'Cursos'

    def __unicode__(self):
        return u'{0} - {1}'.format(self.nome, self.campus)

    # |---------|
    # |Formacao |
    # |---------|
    #     |1
    #     |
    #     |n
    # |------| n     1|-------------|n
    # |Curso |--------|Grupo_Cursos |
    # |------|        |-------------|
    #     |n
    #     |
    #     |1
    # |-------|
    # |Campus |
    # |-------|