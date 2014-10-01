#coding: utf-8
from django.db import models
from django.utils import timezone
from filer.fields.image import FilerImageField

from portal.conteudo.managers import PublicadoManager


class Banner(models.Model):
    sites = models.ManyToManyField('sites.Site', verbose_name=u'Sites para publicação')
    titulo = models.CharField(max_length=250, verbose_name=u'Título', default='')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    url = models.URLField(help_text=u'Insira http://', verbose_name=u'URL')
    arquivo = FilerImageField(verbose_name=u'Imagem', related_name='banners', default=None)
    publicado = models.BooleanField(default=True, verbose_name=u'Publicar')

    objects = models.Manager()
    publicados = PublicadoManager()

    class Meta:
        verbose_name = u'Banner'
        verbose_name_plural = u'Banners'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @property
    def esta_publicado(self):
        return self.publicado and self.data_publicacao < timezone.now()


class BannerAcessoRapido(models.Model):
    sites = models.ManyToManyField('sites.Site', verbose_name=u'Sites para publicação')
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    url = models.URLField(help_text=u'Insira http://', verbose_name=u'URL')
    arquivo = FilerImageField(verbose_name=u'Imagem', related_name='banners_ar', default=None)
    publicado = models.BooleanField(default=True, verbose_name=u'Publicar')

    objects = models.Manager()
    publicados = PublicadoManager()

    class Meta:
        verbose_name = u'Banner de acesso rápido'
        verbose_name_plural = u'Banners de acesso rápido'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @property
    def esta_publicado(self):
        return self.publicado and self.data_publicacao < timezone.now()
