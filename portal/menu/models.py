# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Menu(MPTTModel):
    site = models.ForeignKey('sites.Site')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name=u'Menu pai')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250, blank=True, null=True,
                           help_text=u'Para urls externas utilize o endereço completo. Ex.:'
                                     u'<br>http://www.ifmt.edu.br/'
                                     u'<br><br>Para páginas internas utilize a url gerada na área '
                                     u'de conteúdo/página. Ex.:'
                                     u'<br>/conteudo/pagina/inscricoes-workif/')
    ordem = models.PositiveIntegerField()

    class Meta(object):
        ordering = ('ordem',)
        verbose_name = u'Menu'
        verbose_name_plural = u'Menus'

    class MPTTMeta:
        order_insertion_by = ('ordem', )

    def __unicode__(self):
        return self.titulo
