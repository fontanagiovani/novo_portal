# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.utils import timezone
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from taggit_autosuggest.managers import TaggableManager
from portal.conteudo.managers import ConteudoPublicadoManager


class Conteudo(models.Model):
    campus_origem = models.ForeignKey('core.Campus', verbose_name=u'Origem')
    titulo = models.CharField(max_length=250, verbose_name=u'Título')
    slug = models.SlugField(max_length=250, verbose_name=u'Identificador',
                            help_text=u'Texto que será utilizado para montar a URL deste item')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    galerias = models.ManyToManyField('Galeria', verbose_name=u'Galerias Relacionadas', blank=True)
    videos = models.ManyToManyField('Video', verbose_name=u'Videos Relacionadas', blank=True)
    tags = TaggableManager(blank=True)
    sites = models.ManyToManyField(Site, verbose_name=u'Site(s)')
    publicado = models.BooleanField(default=True, verbose_name=u'Publicar')

    objects = models.Manager()
    publicados = ConteudoPublicadoManager()

    class Meta:
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @property
    def esta_publicado(self):
        return self.publicado and self.data_publicacao < timezone.now()

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
    prioridade_destaque = models.CharField(max_length=1, choices=PRIORIDADE_DESTAQUE, default='6',
                                           verbose_name=u'Prioridade de destaque')
    objects = models.Manager()
    publicados = ConteudoPublicadoManager()

    class Meta:
        verbose_name = u'Notícia'
        verbose_name_plural = u'Notícias'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        if self.esta_publicado:
            return 'conteudo:noticia_detalhe', (), {'slug': self.slug}
        else:
            return 'conteudo:noticia_detalhe_preview', (), {'slug': self.slug}


class Anexo(models.Model):
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='anexos_noticia')
    conteudo = models.ForeignKey('Conteudo', verbose_name=u'conteudo')

    class Meta:
        verbose_name = u'Anexo'
        verbose_name_plural = u'Anexos'

    def __unicode__(self):
        return self.descricao


class Pagina(Conteudo):
    objects = models.Manager()
    publicados = ConteudoPublicadoManager()

    class Meta:
        verbose_name = u'Página'
        verbose_name_plural = u'Páginas'

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        if self.publicado:
            return 'conteudo:pagina_detalhe', (), {'slug': self.slug}
        else:
            return 'conteudo:pagina_detalhe_preview', (), {'slug': self.slug}


class Evento(Conteudo):
    local = models.CharField(max_length=250)
    data_inicio = models.DateTimeField(verbose_name=u'Data de início')
    data_fim = models.DateTimeField(verbose_name=u'Data de término')

    objects = models.Manager()
    publicados = ConteudoPublicadoManager()

    class Meta:
        verbose_name = u'Evento'
        verbose_name_plural = u'Eventos'
        ordering = ('-data_inicio', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        if self.esta_publicado:
            return 'conteudo:evento_detalhe', (), {'slug': self.slug}
        else:
            return 'conteudo:evento_detalhe_preview', (), {'slug': self.slug}


class Licitacao(models.Model):
    TIPO_MODALIDADE = (
        ('1', u'Pregão'),
        ('2', u'Convite'),
        ('3', u'Tomada de preço'),
        ('4', u'Concorrência'),
    )
    sites = models.ManyToManyField(Site, verbose_name=u'Sites para publicação')
    modalidade = models.CharField(max_length=1, choices=TIPO_MODALIDADE, verbose_name=u'Tipo de Modalidade')
    titulo = models.CharField(max_length=100, verbose_name=u'Título')
    data_publicacao = models.DateField(verbose_name=u'Data de publicação')
    data_abertura = models.DateField(verbose_name=u'Data de abertura')
    pregao_srp = models.BooleanField(verbose_name=u'É um pregão SRP?')
    validade_ata_srp = models.DateField(verbose_name=u'Validade ATA SRP', blank=True, null=True)
    possui_contrato = models.BooleanField(verbose_name=u'Possui Contrato?')
    vigencia_contrato_inicio = models.DateField(verbose_name=u'Data de início da vigência do contrato',
                                                blank=True, null=True)
    vigencia_contrato_fim = models.DateField(verbose_name=u'Data de término da vigência do contrato',
                                             blank=True, null=True)
    encerrado = models.BooleanField(verbose_name=u'Processo encerrado?')
    situacao = models.TextField(verbose_name=u'Situação')
    objeto = models.TextField(verbose_name=u'Objeto')
    alteracoes = models.TextField(verbose_name=u'Alterações', blank=True, null=True)
    email_contato = models.EmailField(verbose_name=u'Email para contato')
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = u'Licitação'
        verbose_name_plural = u'Licitações'

    def __unicode__(self):
        return self.titulo

    @staticmethod
    def get_modalidades_existentes(site):
        modalidades_existentes = []
        for modalidade in Licitacao.TIPO_MODALIDADE:
            if Licitacao.objects.filter(sites__exact=site, modalidade=modalidade[0]).exists():
                modalidades_existentes.append(modalidade)

        return modalidades_existentes


class AnexoLicitacao(models.Model):
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição')
    arquivo = FilerFileField(related_name='anexos_licitacao')
    licitacao = models.ForeignKey('Licitacao', verbose_name=u'Licitação')

    class Meta:
        verbose_name = u'Anexo'
        verbose_name_plural = u'Anexos'

    def __unicode__(self):
        return self.descricao


class Video(Conteudo):
    id_video_youtube = models.CharField(max_length=250, verbose_name=u'Id do Video')

    objects = models.Manager()
    publicados = ConteudoPublicadoManager()

    class Meta:
        verbose_name = u'Vídeo'
        verbose_name_plural = u'Vídeos'

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        if self.publicado:
            return 'conteudo:video_detalhe', (), {'slug': self.slug}
        else:
            return 'conteudo:video_detalhe_preview', (), {'slug': self.slug}

    def imagem_sddefault(self):
        return '//i1.ytimg.com/vi/%s/sddefault.jpg' % self.id_video_youtube

    def embed(self):
        return '//www.youtube.com/embed/%s' % self.id_video_youtube


class Galeria(Conteudo):
    objects = models.Manager()
    publicados = ConteudoPublicadoManager()

    class Meta:
        verbose_name = u'Galeria'
        verbose_name_plural = u'Galerias'
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @models.permalink
    def get_absolute_url(self):
        if self.publicado:
            return 'conteudo:galeria_detalhe', (), {'slug': self.slug}
        else:
            return 'conteudo:galeria_detalhe_preview', (), {'slug': self.slug}

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


# work-around para que o signal dos objetos sejam chamados e o index do haystack seja atualizado

# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
#
# @receiver(m2m_changed, sender=Noticia.sites.through)
# def noticia(sender, **kwargs):
#     obj = kwargs['instance']
#     obj.save()
#
#
# @receiver(m2m_changed, sender=Pagina.sites.through)
# def pagina(sender, **kwargs):
#     obj = kwargs['instance']
#     obj.save()
#
#
# @receiver(m2m_changed, sender=Evento.sites.through)
# def evento(sender, **kwargs):
#     obj = kwargs['instance']
#     obj.save()
#
#
# @receiver(m2m_changed, sender=Video.sites.through)
# def video(sender, **kwargs):
#     obj = kwargs['instance']
#     obj.save()
#
#
# @receiver(m2m_changed, sender=Galeria.sites.through)
# def galeria(sender, **kwargs):
#     obj = kwargs['instance']
#     obj.save()