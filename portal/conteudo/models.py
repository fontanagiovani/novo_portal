# -*- coding: utf-8 -*-
from django.db import models
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

CAMPUS_ORIGEM = (
    ('RTR', u'Reitoria'),
    ('BAG', u'Campus Barra do Garças'),
    ('BLV', u'Campus Bela Vista'),
    ('CAS', u'Campus Cáceres'),
    ('CFS', u'Campus Confresa'),
    ('CBA', u'Campus Cuiabá'),
    ('JNA', u'Campus Juína'),
    ('CNP', u'Campus Campo Novo do Parecis'),
    ('PLC', u'Campus Pontes e Lacerda'),
    ('ROO', u'Campus Rondonópolis'),
    ('SVC', u'Campus São Vicente'),
    ('PDL', u'Campus Primavera do Leste'),
    ('SRS', u'Campus Sorriso'),
    ('VGD', u'Campus Várzea Grande'),
    ('AFL', u'Campus Alta Floresta'),
)


class Noticia(models.Model):

    PRIORIDADE_DESTAQUE = (
        ('1', u'1 - Alta'),
        ('2', u'2 - Média-Alta'),
        ('3', u'3 - Média'),
        ('4', u'4 - Baixa-Média'),
        ('5', u'5 - Baixa'),
        ('6', u'Nenhuma')
    )

    campus_origem = models.CharField(max_length=250, choices=CAMPUS_ORIGEM, default='RTR',
                                     verbose_name=u'Campus de origem')
    destaque = models.BooleanField(default=False)
    prioridade_destaque = models.CharField(max_length=1, choices=PRIORIDADE_DESTAQUE, default='6',
                                           verbose_name=u'Prioridade de destaque')
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    fonte = models.CharField(max_length=250, verbose_name=u'Fonte ou Autoria ')

    class Meta:
        verbose_name = u'Notícia'
        verbose_name_plural = u'Notícias'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:noticia_detalhe', (), {'noticia_id': self.id}

    def primeira_imagem(self):
        if self.anexonoticia_set.filter(arquivo__image__isnull=False).exists():
            return self.anexonoticia_set.filter(arquivo__image__isnull=False)[0].arquivo

    def imagens(self):
        if self.anexonoticia_set.filter(arquivo__image__isnull=False).exists():
            return self.anexonoticia_set.filter(arquivo__image__isnull=False)

    def documentos(self):
        if self.anexonoticia_set.filter(arquivo__image__isnull=True).exists():
            return self.anexonoticia_set.filter(arquivo__image__isnull=True)


class AnexoNoticia(models.Model):
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='anexos_noticia')
    noticia = models.ForeignKey('Noticia', verbose_name=u'Notícia')

    class Meta:
        verbose_name = u'Anexo de notícia'
        verbose_name_plural = u'Anexos de notícia'

    def __unicode__(self):
        return self.descricao


class Pagina(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

    class Meta:
        verbose_name = u'Página'
        verbose_name_plural = u'Páginas'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:pagina_detalhe', (), {'pagina_id': self.id}


class AnexoPagina(models.Model):
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='anexos_pagina')
    pagina = models.ForeignKey('Pagina', verbose_name=u'Página')

    class Meta:
        verbose_name = u'Anexo de página'
        verbose_name_plural = u'Anexos de página'

    def __unicode__(self):
        return self.descricao


class Evento(models.Model):

    campus_origem = models.CharField(max_length=250, choices=CAMPUS_ORIGEM, default='RTR',
                                     verbose_name=u'Campus de origem')
    local = models.CharField(max_length=250)
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    data_inicio = models.DateTimeField(verbose_name=u'Data de início')
    data_fim = models.DateTimeField(verbose_name=u'Data de término')

    class Meta:
        verbose_name = u'Evento'
        verbose_name_plural = u'Eventos'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:evento_detalhe', (), {'evento_id': self.id}


class AnexoEvento(models.Model):
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='anexos_evento')
    evento = models.ForeignKey('Evento')

    class Meta:
        verbose_name = u'Anexo de evento'
        verbose_name_plural = u'Anexos de evento'

    def __unicode__(self):
        return self.descricao

class Video(models.Model):

    campus_origem = models.CharField(max_length=250, choices=CAMPUS_ORIGEM, default='RTR', verbose_name=u'Campus de origem')
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    slug = models.SlugField(max_length=250, verbose_name=u'Slug')
    video = models.CharField(max_length=250, verbose_name=u'Id do Video')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    fonte = models.CharField(max_length=250, blank=True, verbose_name=u'Fonte ou Autoria ')

    class Meta:
        verbose_name = u'Vídeo'
        verbose_name_plural = u'Vídeos'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:video_detalhe', (), {'video_id': self.id}

class Galeria(models.Model):

    campus_origem = models.CharField(max_length=250, choices=CAMPUS_ORIGEM, default='RTR', verbose_name=u'Campus de origem')
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    slug = models.SlugField(max_length=250, verbose_name=u'Slug')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    fonte = models.CharField(max_length=250, blank=True, verbose_name=u'Fonte ou Autoria ')

    class Meta:
        verbose_name = u'Galeria'
        verbose_name_plural = u'Galerias'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:galeria_detalhe', (), {'galeria_id': self.id}

    def primeira_imagem(self):
        if self.imagemgaleria_set.filter(arquivo__image__isnull=False).exists():
            return self.imagemgaleria_set.filter(arquivo__image__isnull=False)[0].arquivo

    def imagens(self):
        if self.imagemgaleria_set.filter(arquivo__image__isnull=False).exists():
            return self.imagemgaleria_set.filter(arquivo__image__isnull=False)


class ImagemGaleria(models.Model):
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição')
    imagem = FilerImageField(related_name='Imagem Galeria')
    galeria = models.ForeignKey('Galeria', verbose_name=u'Galeria')

    class Meta:
        verbose_name = u'Anexo de página'
        verbose_name_plural = u'Anexos de página'

    def __unicode__(self):
        return self.descricao