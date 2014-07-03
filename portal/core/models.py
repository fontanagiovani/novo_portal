# -*- coding: utf-8 -*-
from django.db import models
from filer.fields.file import FilerFileField
from mptt.models import MPTTModel, TreeForeignKey


class Conteudo(models.Model):
    TIPOS = (
        ('EVENTO', 'Evento'),
        ('NOTICIA', u'Notícia'),
        ('BANNER', 'Banner'),
    )

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

    tipo = models.CharField(max_length=250, choices=TIPOS, default='NOTICIA')
    campus_origem = models.CharField(max_length=250, choices=CAMPUS_ORIGEM, default='RTR',
                                     verbose_name=u'Campus de origem')
    destaque = models.BooleanField(default=False)
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

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

class Menu(MPTTModel):
    class Meta:
        ordering = ('titulo',)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Nivel 1')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    url  =  models.CharField(max_length=250, blank=True,)

    def __unicode__(self):
        return self.titulo