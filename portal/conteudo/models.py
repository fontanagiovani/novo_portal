# -*- coding: utf-8 -*-
from django.db import models
from filer.fields.file import FilerFileField


class Noticia(models.Model):
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

    class Meta:
        verbose_name = u'Notícia'
        verbose_name_plural = u'Notícias'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'noticia_detalhe', (), {'noticia_id': self.id}

    def primeira_imagem(self):
        if self.anexo_set.filter(arquivo__image__isnull=False).exists():
            return self.anexo_set.filter(arquivo__image__isnull=False)[0].arquivo

    def imagens(self):
        if self.anexo_set.filter(arquivo__image__isnull=False).exists():
            return self.anexo_set.filter(arquivo__image__isnull=False)

    def documentos(self):
        if self.anexo_set.filter(arquivo__image__isnull=True).exists():
            return self.anexo_set.filter(arquivo__image__isnull=True)


class Anexo(models.Model):
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='arquivos')
    noticia = models.ForeignKey('Noticia', verbose_name=u'Notícia')

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