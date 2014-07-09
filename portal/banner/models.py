#coding: utf-8
from django.db import models
from filer.fields.image import FilerImageField
# Create your models here.


class Banner(models.Model):
    titulo=models.CharField(max_length=250, verbose_name=u'Título', null=True, blank=True)
    data_publicacao=models.DateTimeField(verbose_name=u'Data de publicação')
    arquivo=FilerImageField(related_name='midia_banner')

    class Meta:
        verbose_name = u'Banner'
        verbose_name_plural = u'Banners'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.arquivo.name


class BannerAcessoRapido(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    url = models.URLField(max_length=200, verbose_name=u'URL')
    midia_image = FilerImageField(verbose_name=u'Mídia', related_name='ar_banner')


    class Meta:
        verbose_name = u'Banner de acesso rápido'
        verbose_name_plural = u'Banners de acesso rápido'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.titulo



