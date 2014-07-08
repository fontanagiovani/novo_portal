#coding: utf-8
from django.db import models
from filer.fields.file import FilerFileField
# Create your models here.


class Banner(models.Model):
    titulo=models.CharField(max_length=250, verbose_name=u'Título', null=True, blank=True)
    data_publicacao=models.DateTimeField(verbose_name=u'Data de publicação')
    arquivo=FilerFileField(related_name='midia_banner')

    class Meta:
        verbose_name = u'Banner'
        verbose_name_plural = u'Banners'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.arquivo.name


class BannerAcessoRapido(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    midia_image = FilerFileField(verbose_name=u'Mídia', related_name='ar_banner')

    class Meta:
        verbose_name = u'Banner de acesso rápido'
        verbose_name_plural = u'Banners de acesso rápido'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.midia_image.name

    def primeira_imagem(self):
        if self.midia_image.filter(arquivo__image__isnull=False).exists():
            return self.midia_image.filter(arquivo__image__isnull=False)[0].arquivo