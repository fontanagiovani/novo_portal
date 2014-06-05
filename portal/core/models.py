# -*- coding: utf-8 -*-
from django.db import models
from filer.fields.file import FilerFileField


class Conteudo(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    destaque = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Conteúdo'
        verbose_name_plural = u'Conteúdos'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    def primeira_imagem(self):
        if self.midia_set.filter(arquivo__image__isnull=False).exists():
            return self.midia_set.filter(arquivo__image__isnull=False)[0].arquivo


class Midia(models.Model):
    conteudo = models.ForeignKey('Conteudo', verbose_name=u'Conteúdo')
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='arquivos_midia')

    class Meta:
        verbose_name = u'Mídia'
        verbose_name_plural = u'Mídias'

    def __unicode__(self):
        return self.descricao
