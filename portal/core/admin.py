# -*- coding: utf-8 -*-
from django.contrib import admin
from portal.core.models import Menu
from portal.core.models import Selecao


class MenuAdmin(admin.ModelAdmin):
    list_display = ('titulo','parent')
    search_fields = ('titulo',)
    prepopulated_fields = {'slug':('titulo',)}

admin.site.register(Menu,MenuAdmin)

class SelecaoAdmin(admin.ModelAdmin):
    list_display = ('titulo','tipo','status','data_abertura_edital','data_abertura_inscricoes','data_encerramento_inscricoes',)
    search_fields = ('titulo','tipo','status','data_abertura_edital','data_abertura_inscricoes','data_encerramento_inscricoes',)
    date_hierarchy = 'data_abertura_edital'
    list_filter = ('status', 'tipo')
    prepopulated_fields = {'slug':('titulo',)}

admin.site.register(Selecao,SelecaoAdmin)