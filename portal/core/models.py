# -*- coding: utf-8 -*-
import re
from unicodedata import normalize
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from filer.models import File, Image, Folder
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey


class Campus(models.Model):
    nome = models.CharField(max_length=50, verbose_name=u'Nome do Câmpus')

    class Meta:
        verbose_name = _(u'Campus')
        verbose_name_plural = _(u'Campi')

    def __unicode__(self):
        return self.nome


class TipoSelecao(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Tipo pai')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name=u'Identificador')

    class Meta:
        ordering = ('titulo',)
        verbose_name = _(u'Tipo de selecao')
        verbose_name_plural = _(u'Tipos de selecao')

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
        verbose_name = _(u'Selecao')
        verbose_name_plural = _(u'Selecoes')

    def __unicode__(self):
        return self.titulo


class SiteDetalhe(models.Model):
    site = models.OneToOneField('sites.Site')
    campus = models.ForeignKey('Campus', help_text=u'Câmpus ou local que este site está relacionado')
    destino = models.ForeignKey('Destino', help_text=u'Destino da página inicial')
    logo = FilerImageField()
    disqus_shortname = models.CharField(max_length=250, null=True, blank=True,
                                        help_text=u'ShortName do site no serviço de comentários DISQUS')
    hotsite = models.BooleanField(default=False)
    hotsite_background = FilerImageField(null=True, blank=True, related_name='hotsite_background_SiteDetalhe', verbose_name=u'Background do hotsite')
    modal = models.TextField(null=True, blank=True)
    social = models.TextField(null=True, blank=True)
    links_uteis = models.TextField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.site.domain


class Destino(models.Model):
    TIPO = (
        ('PORTAL', u'PORTAL'),
        ('PORTAL_SECUNDARIO', u'PORTAL SECUNDÁRIO'),
        ('BLOG', u'BLOG'),
        ('BLOG_SLIDER', u'BLOG SLIDER'),
        ('PAGINA', u'PÁGINA INDIVIDUAL'),
        ('INDEPENDENTE', u'PORTAL INDEPENDENTE'),
        ('REDIRECT', u'REDIRECIONAMENTO'),
    )

    tipo = models.CharField(max_length=100, choices=TIPO)
    caminho = models.CharField(max_length=200, help_text=u'Utilize o caminho app/template - Templates disponíveis:'
                                                         u'<br>core/portal.html'
                                                         u'<br>core/portal_secundario.html'
                                                         u'<br>core/blog.html'
                                                         u'<br>core/blog_slider.html'
                                                         u'<br>core/pagina.html'
                                                         u'<br>core/independente.html'
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
    def pagina():
        return 'PAGINA'

    @staticmethod
    def independente():
        return 'INDEPENDENTE'

    @staticmethod
    def redirect():
        return 'REDIRECT'


class ContadorVisitas(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_em = models.DateTimeField(auto_now=True, editable=False)
    url = models.CharField(max_length=2000)
    contagem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-contagem', '-criado_em', '-modificado_em')
        get_latest_by = 'criado_em'
        verbose_name = _(u'Contador de visitas')
        verbose_name_plural = _(u'Contador de visitas')

    def __unicode__(self):
        return self.url


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
