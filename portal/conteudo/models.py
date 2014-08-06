# -*- coding: utf-8 -*-
from django.db import models
from portal.core.models import Campus
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager
#
# CAMPUS_ORIGEM = (
#     ('RTR', u'Reitoria'),
#     ('BAG', u'Campus Barra do Garças'),
#     ('BLV', u'Campus Bela Vista'),
#     ('CAS', u'Campus Cáceres'),
#     ('CFS', u'Campus Confresa'),
#     ('CBA', u'Campus Cuiabá'),
#     ('JNA', u'Campus Juína'),
#     ('CNP', u'Campus Campo Novo do Parecis'),
#     ('PLC', u'Campus Pontes e Lacerda'),
#     ('ROO', u'Campus Rondonópolis'),
#     ('SVC', u'Campus São Vicente'),
#     ('PDL', u'Campus Primavera do Leste'),
#     ('SRS', u'Campus Sorriso'),
#     ('VGD', u'Campus Várzea Grande'),
#     ('AFL', u'Campus Alta Floresta'),
# )


class Conteudo(models.Model):

    campus_origem = models.ForeignKey('core.Campus', verbose_name=u'Campus de origem')
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    slug = models.SlugField(max_length=250, verbose_name=u'Slug')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    fonte = models.CharField(max_length=250, blank=True, verbose_name=u'Fonte ou Autoria ')
    galerias = models.ManyToManyField('Galeria', verbose_name=u'Galerias Relacionadas', blank=True)
    videos = models.ManyToManyField('Video', verbose_name=u'Videos Relacionadas', blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    def primeira_imagem(self):
        if self.anexo_set.filter(arquivo__image__isnull=False).exists():
            return self.anexo_set.filter(arquivo__image__isnull=False)[0].arquivo

    def imagens(self):
        if self.anexo_set.filter(arquivo__image__isnull=False).exists():
            return self.anexo_set.filter(arquivo__image__isnull=False)

    def documentos(self):
        if self.anexo_set.filter(arquivo__image__isnull=True).exists():
            return self.anexo_set.filter(arquivo__image__isnull=True)


class Noticia(Conteudo):

    PRIORIDADE_DESTAQUE = (
        ('1', u'1 - Alta'),
        ('2', u'2 - Média-Alta'),
        ('3', u'3 - Média'),
        ('4', u'4 - Baixa-Média'),
        ('5', u'5 - Baixa'),
        ('6', u'Nenhuma')
    )

    destaque = models.BooleanField(default=False)
    prioridade_destaque = models.CharField(max_length=1, choices=PRIORIDADE_DESTAQUE, default='6',verbose_name=u'Prioridade de destaque')

    class Meta:
        verbose_name = u'Notícia'
        verbose_name_plural = u'Notícias'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:noticia_detalhe', (), {'noticia_id': self.id}


class Anexo(models.Model):
    descricao = models.TextField(verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='anexos_noticia')
    conteudo = models.ForeignKey('Conteudo', verbose_name=u'conteudo')

    class Meta:
        verbose_name = u'Anexo'
        verbose_name_plural = u'Anexos'

    def __unicode__(self):
        return self.descricao


class Pagina(Conteudo):

    class Meta:
        verbose_name = u'Página'
        verbose_name_plural = u'Páginas'

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:pagina_detalhe', (), {'pagina_id': self.id}


class Evento(Conteudo):

    local = models.CharField(max_length=250)
    data_inicio = models.DateTimeField(verbose_name=u'Data de início')
    data_fim = models.DateTimeField(verbose_name=u'Data de término')

    class Meta:
        verbose_name = u'Evento'
        verbose_name_plural = u'Eventos'
        ordering = ('-data_inicio', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:evento_detalhe', (), {'evento_id': self.id}


class Video(Conteudo):

    id_video_youtube = models.CharField(max_length=250, verbose_name=u'Id do Video')

    class Meta:
        verbose_name = u'Vídeo'
        verbose_name_plural = u'Vídeos'

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        return 'conteudo:video_detalhe', (), {'video_id': self.id}

    def imagem_sddefault(self):
        return '//i1.ytimg.com/vi/%s/sddefault.jpg' % self.id_video_youtube

    def embed(self):
        return '//www.youtube.com/embed/%s' % self.id_video_youtube


class Galeria(Conteudo):

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
        if self.imagemgaleria_set.all().exists():
            return self.imagemgaleria_set.all()[0].imagem

    def imagens(self):
        if self.imagemgaleria_set.all().exists():
            return self.imagemgaleria_set.all()


class ImagemGaleria(models.Model):
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição')
    imagem = FilerImageField(related_name='Imagem Galeria')
    galeria = models.ForeignKey('Galeria', verbose_name=u'Galeria')

    class Meta:
        verbose_name = u'Anexo de página'
        verbose_name_plural = u'Anexos de página'

    def __unicode__(self):
        return self.descricao

