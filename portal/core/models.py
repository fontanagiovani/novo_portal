# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# from topnotchdev import files_widget
# from filebrowser.fields import FileBrowseField
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField


class Curso(models.Model):
    CHOICES_CAMPUS = (
        ('CNP', u'Campus Campo Novo do Parecis'),
        ('CBA', u'Campus Cuiabá'),
        ('BLV', u'Campus Bela Vista')
    )

    CHOICES_NIVEL = (
        ('POS', 'Pós-Graduação'),
        ('SUP', 'Superior'),
        ('TSS', 'Técnico Subsequente'),
        ('TIM', 'Técnico Integrado ao Ensino Médio'),
        ('TIP', 'Técnico Integrado ao Ensino Médio Modalidade PROEJA')
    )

    campus = models.CharField(max_length=3, choices=CHOICES_CAMPUS)
    nivel = models.CharField(max_length=200, choices=CHOICES_NIVEL)
    nome = models.CharField(max_length=300)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = u'Curso'
        verbose_name_plural = u'Cursos'

    def __unicode__(self):
        return '%s - %s' % (self.campus, self.nome)


class Site(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Site pai')
    nome = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name = u'Site'
        verbose_name_plural = u'Sites'

    def __unicode__(self):
        return self.slug


class Menu(MPTTModel):
    sites = models.ManyToManyField('Site')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Menu pai')
    menucontainer = models.ForeignKey('MenuContainer', verbose_name='Container')
    titulo = models.CharField(max_length=50)
    ordem = models.IntegerField()
    link = models.URLField(null=True, blank=True,
                           help_text=u'Informe o link completo - Ex.: http://www.ifmt.edu.br')
    pagina = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = u'Menu'
        verbose_name_plural = u'Menus'

    def __unicode__(self):
        return self.titulo


class MenuContainer(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = u'Menu container'
        verbose_name_plural = u'Menus container'

    def __unicode__(self):
        return self.nome


class Pagina(models.Model):
    sites = models.ManyToManyField('Site')
    titulo = models.CharField(max_length=250)
    texto = models.TextField()
    data_postagem = models.DateTimeField()

    class Meta:
        verbose_name = u'Página'
        verbose_name_plural = u'Páginas'

    def __unicode__(self):
        return self.titulo


class Midia(models.Model):
    descricao = models.TextField()
    imagem = FilerImageField(null=True, blank=True, related_name='imagem')
    arquivo = FilerFileField(null=True, blank=True, related_name='arquivo')
    # arquivo = models.FileField(upload_to='%d_%d' % (datetime.today().year, datetime.today().month))
    # imagens_files_widget = files_widget.ImageField(blank=True, null=True)
    # arquivos_files_widget = files_widget.FileField(blank=True, null=True)
    # imagem_filebrowser = FileBrowseField("Imagem", max_length=200, directory='imagens/', blank=True, null=True,
    #                                      extensions=['.jpg', '.jpeg', '.gif', '.png'])
    # arquivo_filebrowser = FileBrowseField("Documento", max_length=200, directory='documentos/', blank=True,
    #                                       extensions=['.pdf', '.doc', '.*'],  null=True)

    class Meta:
        verbose_name = u'Mídia'
        verbose_name_plural = u'Mídias'

    def __unicode__(self):
        return self.descricao


class MidiaPagina(Midia):
    pagina = models.ForeignKey('Pagina')

    class Meta:
        verbose_name = u'Mídia da página'
        verbose_name_plural = u'Mídias da página'


@receiver(post_delete, sender=Midia)
def midia_delete(sender, instance, **kwargs):
    """
    Signal post_delete para remover o arquivo do disco quando uma Midia e apagada
    """
    # Pass false so FileField doesn't save the model.
    instance.arquivo.delete(False)
