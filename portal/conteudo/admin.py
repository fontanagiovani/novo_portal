# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.conteudo.models import Noticia
from portal.conteudo.models import Anexo
from portal.conteudo.forms import NoticiaForm


class AnexoInLine(admin.StackedInline):
    model = Anexo
    extra = 1


class NoticiaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'destaque', 'prioridade_destaque')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('destaque', )

    form = NoticiaForm

    inlines = (AnexoInLine, )

admin.site.register(Noticia, NoticiaAdmin)