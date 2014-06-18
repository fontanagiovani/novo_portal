# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.conteudo.models import Noticia
from portal.conteudo.models import MidiaNoticia
from portal.conteudo.forms import NoticiaForm


class MidiaNoticiaInLine(admin.StackedInline):
    model = MidiaNoticia
    extra = 0


class NoticiaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'destaque')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('destaque', )

    form = NoticiaForm

    inlines = (MidiaNoticiaInLine, )

admin.site.register(Noticia, NoticiaAdmin)