# -*- coding: utf-8 -*-
from django.db import models
from filer.fields.file import FilerFileField


class Conteudo(models.Model):
    titulo = models.CharField(max_length=250)
    texto = models.TextField()
    data_publicacao = models.DateTimeField()

    class Meta:
        verbose_name = u'Página'
        verbose_name_plural = u'Páginas'

    def __unicode__(self):
        return self.titulo


class Midia(models.Model):
    pagina = models.ForeignKey('Conteudo')
    descricao = models.TextField()
    arquivo = FilerFileField(null=True, blank=True, related_name='arquivos_midia')

    class Meta:
        verbose_name = u'Mídia'
        verbose_name_plural = u'Mídias'

    def __unicode__(self):
        return self.descricao
