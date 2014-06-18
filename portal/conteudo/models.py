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
    )

    campus_origem = models.CharField(max_length=250, choices=CAMPUS_ORIGEM, default='RTR',
                                     verbose_name=u'Campus de origem')
    destaque = models.BooleanField(default=False)
    prioridade_destaque = models.CharField(max_length=1, choices=PRIORIDADE_DESTAQUE, default='5',
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


class Banner(models.Model):
    titulo = models.CharField(max_length=250, verbose_name=u'Título')


class Evento(Noticia):
    class Meta:
        verbose_name = u'Evento'
        verbose_name_plural = u'Eventos'


class Midia(models.Model):
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='arquivos')

    class Meta:
        verbose_name = u'Mídia'
        verbose_name_plural = u'Mídias'

    def __unicode__(self):
        return self.descricao


class MidiaNoticia(Midia):
    noticia = models.ForeignKey('Noticia', verbose_name=u'Notícia')


class MidiaBanner(Midia):
    banner = models.ForeignKey('Banner', verbose_name=u'Banner')


class MidiaEvento(Midia):
    evento = models.ForeignKey('Evento', verbose_name=u'Evento')
