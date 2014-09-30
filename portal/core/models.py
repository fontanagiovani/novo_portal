# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from filer.fields.image import FilerImageField


class Campus(models.Model):
    nome = models.CharField(max_length=50, verbose_name=u'Nome do Câmpus')

    class Meta:
        verbose_name = u'Campus'
        verbose_name_plural = u'Campi'

    def __unicode__(self):
        return self.nome


class Menu(MPTTModel):
    site = models.ForeignKey('sites.Site')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name=u'Menu pai')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250)
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
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Tipo pai')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name=u'Identificador')

    class Meta:
        ordering = ('titulo',)
        verbose_name = u'Tipo de seleção'
        verbose_name_plural = u'Tipos de seleção'

    def __unicode__(self):
        return self.titulo


class Selecao(models.Model):
    STATUS = (
        ('ABT', 'Aberto'),
        ('AND', 'Em Andamento'),
        ('FNZ', 'Finalizado')
    )

    tipo = TreeForeignKey('TipoSelecao')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250,)
    status = models.CharField(max_length=3, choices=STATUS)
    data_abertura_edital = models.DateTimeField(verbose_name=u'Data de Abertura do Edital')
    data_abertura_inscricoes = models.DateTimeField(verbose_name=u'Data de Abertura de Inscrições')
    data_encerramento_inscricoes = models.DateTimeField(verbose_name=u'Data de Fechamento das Incrições')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

    class Meta:
        ordering = ('titulo', 'status', 'data_abertura_edital')
        verbose_name = u'Seleção'
        verbose_name_plural = u'Seleções'

    def __unicode__(self):
        return self.titulo


class SiteDetalhe(models.Model):
    site = models.OneToOneField('sites.Site')
    campus = models.ForeignKey('Campus', help_text=u'Câmpus ou local que este site está relacionado')
    destino = models.ForeignKey('Destino', help_text=u'Destino da página inicial')
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
