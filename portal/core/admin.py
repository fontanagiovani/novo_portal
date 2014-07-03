# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.core.models import Conteudo
from portal.core.models import Midia
from portal.core.models import Menu


class MidiaInLine(admin.StackedInline):
    model = Midia
    extra = 0


class ConteudoAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'tipo', 'destaque')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('tipo', 'destaque')

    inlines = (MidiaInLine, )

admin.site.register(Conteudo, ConteudoAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('titulo','parent')
    search_fields = ('titulo',)
    prepopulated_fields = {'slug':('titulo',)}

admin.site.register(Menu,MenuAdmin)