#coding: utf-8
from django.db import models
from filer.fields.file import FilerFileField
# Create your models here.


class Banner(models.Model):
    titulo=models.CharField(max_length=250, verbose_name=u'Título', blank=True)
    data_publicacao=models.DateTimeField(verbose_name=u'Data de publicação')
    descricao=models.CharField(max_length=250, verbose_name=u'Descrição', default='') #deve ser alterado para not blank
    arquivo=FilerFileField(related_name='midia_banner')

    class Meta:
        verbose_name = u'Banner'
        verbose_name_plural = u'Banners'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
      return self.descricao