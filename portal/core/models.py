# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class Campus(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Nivel 1')
    sigla = models.CharField(max_length=3, verbose_name=u'Sigla do Campus')
    nome = models.CharField(max_length=50, verbose_name=u'Nome do Campus')
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name = u'Campus'
        verbose_name_plural = u'Campi'

    def __unicode__(self):
        return self.nome


class Menu(MPTTModel):
    site = models.ForeignKey(Site)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name=u'Menu pai')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    url = models.CharField(max_length=250, blank=True,)
    ordem = models.PositiveIntegerField()

    class Meta(object):
        ordering = ('ordem',)

    class MPTTMeta:
        order_insertion_by = ('ordem', )

    def __unicode__(self):
        return self.titulo

    def menu_raiz(self):
        if self.parent is None:
            return ""
        return self.parent


class TipoSelecao(MPTTModel):
    class Meta:
        ordering = ('titulo',)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Tipo pai')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return self.titulo


class Selecao(models.Model):

    STATUS = (
        ('ABT', 'Aberto'),
        ('AND', 'Em Andamento'),
        ('FNZ', 'Finalizado')
    )

    class Meta:
        ordering = ('titulo', 'status', 'data_abertura_edital')

    tipo = TreeForeignKey('TipoSelecao')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250,)
    status = models.CharField(max_length=3, choices=STATUS)
    data_abertura_edital = models.DateTimeField(verbose_name=u'Data de Abertura do Edital')
    data_abertura_inscricoes = models.DateTimeField(verbose_name=u'Data de Abertura de Inscrições')
    data_encerramento_inscricoes = models.DateTimeField(verbose_name=u'Data de Fechamento das Incrições')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

    def __unicode__(self):
        return self.titulo


class PermissaoPublicacao(models.Model):
    class Meta:
        verbose_name = u'Permissão de Publicacão'
        verbose_name_plural = u'Permissões de Publicação'

    sites = models.ManyToManyField(Site, verbose_name=u'Sites Permitidos')
    user = models.OneToOneField(User, verbose_name=u'Usuario', primary_key=True)


class SiteDetalhe(models.Model):
    site = models.OneToOneField(Site)
    template = models.ForeignKey('Template', help_text=u'Template da página inicial')
    endereco = models.CharField(max_length=200)


class Template(models.Model):
    DESC = (
        ('PORTAL', u'Portal'),
        ('CAMPUS', u'Câmpus'),
        ('BLOG', u'Blog'),
        ('PAGINA', u'Página individual'),
    )

    descricao = models.CharField(max_length=30, choices=DESC)
    caminho = models.CharField(max_length=100, help_text=u'Utilize o caminho app/template - Ex.: core/portal.html')

    def __unicode__(self):
        return self.descricao


def portal():
    return Template.DESC[0][0]


def campus():
    return Template.DESC[1][0]


def blog():
    return Template.DESC[2][0]


def pagina():
    return Template.DESC[3][0]