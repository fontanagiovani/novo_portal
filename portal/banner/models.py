#coding: utf-8
from django.db import models
from filer.fields.image import FilerImageField



class Banner(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    arquivo = FilerImageField(related_name='midia_banner', default=None)

    class Meta:
        verbose_name = u'Banner'
        verbose_name_plural = u'Banners'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.titulo


class BannerAcessoRapido(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    url = models.URLField(help_text=u'Insira http://', max_length=200, verbose_name=u'URL')
    midia_image = FilerImageField(verbose_name=u'Mídia', related_name='ar_banner', default=None)


    class Meta:
        verbose_name = u'Banner de acesso rápido'
        verbose_name_plural = u'Banners de acesso rápido'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.titulo



