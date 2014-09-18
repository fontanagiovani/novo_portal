# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from mptt.admin import MPTTModelAdmin
from adminsortable.admin import SortableAdminMixin

from portal.core.models import Menu
from portal.core.models import SiteDetalhe
from portal.core.models import Template
from portal.core.models import Campus
from portal.core.models import Selecao, TipoSelecao
from portal.core.forms import MenuForm
from portal.core.forms import SiteDetalheForm, SiteDetalheFormset


class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'parent',)
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
        modelform = super(MenuAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)

        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(MenuAdmin, self).queryset(request)
        return qs.filter(site__in=request.user.permissao.sites.all()).distinct()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "site":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(MenuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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


class SiteIndexInline(admin.StackedInline):
    model = SiteDetalhe
    form = SiteDetalheForm
    formset = SiteDetalheFormset

    max_num = 1
    can_delete = False


class SiteIndexAdmin(SiteAdmin):

    inlines = [SiteIndexInline]

admin.site.unregister(Site)
admin.site.register(Site, SiteIndexAdmin)


class TemplateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Template, TemplateAdmin)
