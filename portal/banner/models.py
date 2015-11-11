# coding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField

from portal.banner.managers import PublicadoManager, DestaqueManager, LinkDeAcessoManager, GovernamentalManager, \
    HotsiteManager


class Banner(models.Model):
    TIPO = (
        ('1', 'Destaque'),
        ('2', 'Link de acesso'),
        ('3', 'Governamental'),
        ('4', 'Hotsite'),
    )

    sites = models.ManyToManyField('sites.Site', verbose_name=u'Sites para publicação')
    tipo = models.CharField(max_length=2, default=1, choices=TIPO)
    titulo = models.CharField(max_length=250, verbose_name=u'Título', default='')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')
    url = models.CharField(max_length=250,
                           help_text=u'Para urls externas utilize o endereço completo. Ex.:'
                                     u'<br>http://www.ifmt.edu.br/'
                                     u'<br><br>Para páginas internas utilize a url gerada na área '
                                     u'de conteúdo/página. Ex.:'
                                     u'<br>/conteudo/pagina/inscricoes-workif/')
    arquivo = FilerImageField(verbose_name=u'Imagem', related_name='banners', default=None)
    nova_janela = models.BooleanField(default=False, verbose_name=u'Abrir em uma nova janela?')
    publicado = models.BooleanField(default=True, verbose_name=u'Publicar')

    objects = models.Manager()
    publicados = PublicadoManager()
    destaque = DestaqueManager()
    linkdeacesso = LinkDeAcessoManager()
    governamental = GovernamentalManager()
    hotsite = HotsiteManager()

    class Meta:
        verbose_name = _(u'Banner')
        verbose_name_plural = _(u'Banners')
        ordering = ('-data_publicacao', '-id')

    def __unicode__(self):
        return self.titulo

    @property
    def esta_publicado(self):
        return self.publicado and self.data_publicacao < timezone.now()
