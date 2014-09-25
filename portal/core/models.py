# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from mptt.models import MPTTModel, TreeForeignKey
from filer.fields.image import FilerImageField


class Campus(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Nivel 1')
    sigla = models.CharField(max_length=3, verbose_name=u'Sigla do Campus')
    nome = models.CharField(max_length=50, verbose_name=u'Nome do Campus')
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    site = models.OneToOneField(Site, verbose_name='Link de origem', default=None, null=True)

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


class SiteDetalhe(models.Model):
    site = models.OneToOneField(Site)
    destino = models.ForeignKey('Destino', help_text=u'Template da página inicial')
    logo = FilerImageField()
    social = models.TextField(null=True, blank=True)
    links_uteis = models.TextField(null=True, blank=True)
    mapa_site = models.TextField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.site.domain


class Destino(models.Model):
    TIPO = (
        ('PORTAL', u'PORTAL'),
        ('CAMPUS', u'CMPUS'),
        ('BLOG', u'Blog'),
        ('PAGINA', u'Página individual'),
        ('REDIRECT', u'Redirect'),
    )

    tipo = models.CharField(max_length=100, choices=TIPO)
    caminho = models.CharField(max_length=200, help_text=u'Utilize o caminho app/template - Ex.: core/portal.html'
                                                         u'<br>Em caso de redirect use a url completa - '
                                                         u'Ex.: http://www.ifmt.edu.br')

    def __unicode__(self):
        return '%s: %s' % (self.tipo, self.caminho)

    @staticmethod
    def portal():
        return Destino.TIPO[0][0]

    @staticmethod
    def campus():
        return Destino.TIPO[1][0]

    @staticmethod
    def blog():
        return Destino.TIPO[2][0]

    @staticmethod
    def pagina():
        return Destino.TIPO[3][0]

    @staticmethod
    def redirect():
        return Destino.TIPO[4][0]
