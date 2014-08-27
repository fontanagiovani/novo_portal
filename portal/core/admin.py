# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from portal.core.models import Menu
from portal.core.models import Campus
from portal.core.models import Selecao, TipoSelecao
from portal.core.models import PermissaoPublicacao
from django.contrib.auth.admin import User
from django.contrib.auth.admin import UserAdmin


class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome', 'parent',)
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}

admin.site.register(Campus, CampusAdmin)


class MenuAdmin(MPTTModelAdmin):
    list_display = ('titulo', 'menu_raiz', 'ordem',)
    search_fields = ('titulo',)
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(Menu, MenuAdmin)


class TipoSelecaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'parent',)
    search_fields = ('titulo',)
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(TipoSelecao, TipoSelecaoAdmin)


class SelecaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'status', 'data_abertura_edital', 'data_abertura_inscricoes',
                    'data_encerramento_inscricoes', )
    search_fields = ('titulo', 'tipo', 'status', 'data_abertura_edital', 'data_abertura_inscricoes',
                     'data_encerramento_inscricoes', )
    date_hierarchy = 'data_abertura_edital'
    list_filter = ('status', 'tipo')

admin.site.register(Selecao, SelecaoAdmin)


class SiteInline(admin.StackedInline):
    model = PermissaoPublicacao
    max_num = 1
    can_delete = False


class UserAdmin(UserAdmin):
    #
    # def add_view(self, *args, **kwargs):
    #     self.\
    inlines = [SiteInline]
    #             = []
    #     return super(SiteInline, self).add_view(*args, **kwargs)
    #
    # def change_view(self, *args, **kwargs):
    #     self.inline)instance.append()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)



