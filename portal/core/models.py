# -*- coding: utf-8 -*-
from django.db import models
from filer.fields.file import FilerFileField


class Conteudo(models.Model):
    CONTENT_TYPE = (
        ('EVENTOS', 'Eventos'),
        ('NOTICIAS', u'Notícias'),
        ('BANNER', 'Banner'),
    )

    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    destaque = models.BooleanField(default=False)
    tipo = models.CharField(max_length=250, choices=CONTENT_TYPE, default='NOTICIAS')

    class Meta:
        verbose_name = u'Conteúdo'
        verbose_name_plural = u'Conteúdos'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo_detalhe', (), {'conteudo_id': self.id}

    def primeira_imagem(self):
        if self.midia_set.filter(arquivo__image__isnull=False).exists():
            return self.midia_set.filter(arquivo__image__isnull=False)[0].arquivo

    def imagens(self):
        if self.midia_set.filter(arquivo__image__isnull=False).exists():
            return self.midia_set.filter(arquivo__image__isnull=False)

    def documentos(self):
        if self.midia_set.filter(arquivo__image__isnull=True).exists():
            return self.midia_set.filter(arquivo__image__isnull=True)


class Midia(models.Model):
    conteudo = models.ForeignKey('Conteudo', verbose_name=u'Conteúdo')
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='arquivos_midia')

    class Meta:
        verbose_name = u'Mídia'
        verbose_name_plural = u'Mídias'

    def __unicode__(self):
        return self.descricao
