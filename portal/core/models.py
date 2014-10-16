# -*- coding: utf-8 -*-
import re
from unicodedata import normalize
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from filer.models import File, Image, Folder
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey


class Campus(models.Model):
    nome = models.CharField(max_length=50, verbose_name=u'Nome do Câmpus')

    class Meta:
        verbose_name = u'Campus'
        verbose_name_plural = u'Campi'

    def __unicode__(self):
        return self.nome


class Menu(MPTTModel):
    site = models.ForeignKey('sites.Site')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name=u'Menu pai')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250)
    ordem = models.PositiveIntegerField()

    class Meta(object):
        ordering = ('ordem',)

    class MPTTMeta:
        order_insertion_by = ('ordem', )

    def __unicode__(self):
        return self.titulo

    def menu_raiz(self):
        if self.parent is None:
            return ""
        return self.parent


class TipoSelecao(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Tipo pai')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name=u'Identificador')

    class Meta:
        ordering = ('titulo',)
        verbose_name = u'Tipo de seleção'
        verbose_name_plural = u'Tipos de seleção'

    def __unicode__(self):
        return self.titulo


class Selecao(models.Model):
    STATUS = (
        ('ABT', 'Aberto'),
        ('AND', 'Em Andamento'),
        ('FNZ', 'Finalizado')
    )

    tipo = TreeForeignKey('TipoSelecao')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250,)
    status = models.CharField(max_length=3, choices=STATUS)
    data_abertura_edital = models.DateTimeField(verbose_name=u'Data de Abertura do Edital')
    data_abertura_inscricoes = models.DateTimeField(verbose_name=u'Data de Abertura de Inscrições')
    data_encerramento_inscricoes = models.DateTimeField(verbose_name=u'Data de Fechamento das Incrições')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

    class Meta:
        ordering = ('titulo', 'status', 'data_abertura_edital')
        verbose_name = u'Seleção'
        verbose_name_plural = u'Seleções'

    def __unicode__(self):
        return self.titulo


class SiteDetalhe(models.Model):
    site = models.OneToOneField('sites.Site')
    campus = models.ForeignKey('Campus', help_text=u'Câmpus ou local que este site está relacionado')
    destino = models.ForeignKey('Destino', help_text=u'Destino da página inicial')
    logo = FilerImageField()
    modal = models.TextField(null=True, blank=True)
    social = models.TextField(null=True, blank=True)
    links_uteis = models.TextField(null=True, blank=True)
    mapa_site = models.TextField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.site.domain


class Destino(models.Model):
    TIPO = (
        ('PORTAL', u'PORTAL'),
        ('PORTAL_SECUNDARIO', u'PORTAL SECUNDÁRIO'),
        ('BLOG', u'BLOG'),
        ('BLOG_SLIDER', u'BLOG SLIDER'),
        ('BANNERS', u'BANNERS'),
        ('REDIRECT', u'REDIRECIONAMENTO'),
    )

    tipo = models.CharField(max_length=100, choices=TIPO)
    caminho = models.CharField(max_length=200, help_text=u'Utilize o caminho app/template - Templates disponíveis:'
                                                         u'<br>core/portal.html'
                                                         u'<br>core/portal_secundario.html'
                                                         u'<br>core/blog.html'
                                                         u'<br>core/blog_slider.html'
                                                         u'<br>core/banners.html'
                                                         u'<br><br>Em caso de redirect use a url completa - '
                                                         u'Ex.: http://www.ifmt.edu.br')

    def __unicode__(self):
        return '%s: %s' % (self.tipo, self.caminho)

    @staticmethod
    def portal():
        return 'PORTAL'

    @staticmethod
    def portal_secundario():
        return 'PORTAL_SECUNDARIO'

    @staticmethod
    def blog():
        return 'BLOG'

    @staticmethod
    def blog_slider():
        return 'BLOG_SLIDER'

    @staticmethod
    def banners():
        return 'BANNERS'

    @staticmethod
    def redirect():
        return 'REDIRECT'


# cria um diretorio no filer para cada novo usuario
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        diretorio = Folder(
            owner=instance,
            name=instance.username,
        )
        diretorio.save()

post_save.connect(create_user_profile, sender=User)


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_ºª`{|},:]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def unicode_filename(sender, instance, created, **kwargs):
    if instance.original_filename:
        if not instance.original_filename == slugify(instance.original_filename):
            instance.original_filename = slugify(instance.original_filename)
            instance.save()

post_save.connect(unicode_filename, sender=File)
post_save.connect(unicode_filename, sender=Image)