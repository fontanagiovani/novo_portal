# -*- coding: utf-8 -*-
from Crypto.SelfTest.Cipher.test_pkcs1_15 import t2b
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from adminsortable.admin import SortableAdminMixin
from portal.core.models import Menu
from portal.core.models import Campus
from portal.core.models import Selecao, TipoSelecao
from portal.core.models import PermissaoPublicacao
from portal.core.forms import MenuForm
from django.contrib.auth.admin import User
from django.contrib.auth.admin import UserAdmin


class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome', 'parent',)
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}

admin.site.register(Campus, CampusAdmin)


class MenuAdmin(SortableAdminMixin, MPTTModelAdmin):
    """
    Para obter a renderizacao adequada a classe deve herdar de SortableAdminMixin e MPTTModelAdmin nesta ordem
    e o atributo change_list_template deve ser definido para sobrescrever os definidos pela classes
    SortableAdminMixin e MPTTModelAdmin pela juncao dos dois templates
    """
    list_display = ('titulo', 'menu_raiz', 'site')
    search_fields = ('titulo',)
    prepopulated_fields = {'slug': ('titulo',)}
    list_filter = ('site', )

    change_list_template = 'core/mptt_sortable_change_list.html'
    add_form_template = 'core/mptt_sortable_change_form.html'
    change_form_template = 'core/mptt_sortable_change_form.html'

    form = MenuForm

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(MenuAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


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


class PermissaoPublicacaoAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'sites_publicacao')
    inlines = [SiteInline]

    def sites_publicacao(self, obj):
        sites_perm = []
        for site in obj.permissaopublicacao.sites.all():
            sites_perm.append(site)
        if sites_perm == []:
            return ""
        else:
            return sites_perm

admin.site.unregister(User)
admin.site.register(User, PermissaoPublicacaoAdmin)



