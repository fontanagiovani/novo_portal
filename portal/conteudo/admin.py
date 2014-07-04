# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.conteudo.models import Noticia
from portal.conteudo.models import Pagina
from portal.conteudo.models import AnexoNoticia
from portal.conteudo.models import AnexoPagina
from portal.conteudo.forms import NoticiaForm


class AnexoNoticiaInLine(admin.StackedInline):
    model = AnexoNoticia
    extra = 1


class NoticiaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'destaque', 'prioridade_destaque')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('destaque', 'prioridade_destaque')

    form = NoticiaForm

    inlines = (AnexoNoticiaInLine, )

admin.site.register(Noticia, NoticiaAdmin)


class AnexoPaginaInLine(admin.StackedInline):
    model = AnexoPagina
    extra = 1


class PaginaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'get_link')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'

    inlines = (AnexoPaginaInLine, )

    def get_link(self, obj):
        return obj.get_absolute_url()
    get_link.short_description = u'Link da página'

admin.site.register(Pagina, PaginaAdmin)