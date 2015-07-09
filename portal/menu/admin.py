# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from adminsortable.admin import SortableAdminMixin
import reversion

from portal.core.admin import SiteListFilter
from portal.menu.models import Menu
from portal.menu.forms import MenuForm


class MenuAdmin(reversion.VersionAdmin, SortableAdminMixin, MPTTModelAdmin):
    """
    Para obter a renderizacao adequada a classe deve herdar de SortableAdminMixin e MPTTModelAdmin nesta ordem
    e o atributo change_list_template deve ser definido para sobrescrever os definidos pela classes
    SortableAdminMixin e MPTTModelAdmin pela juncao dos dois templates
    """
    list_display = ('titulo', 'menu_pai', 'site')
    search_fields = ('titulo',)
    list_filter = (SiteListFilter, )

    change_list_template = 'menu/mptt_sortable_change_list.html'
    add_form_template = 'menu/mptt_sortable_change_form.html'
    change_form_template = 'menu/mptt_sortable_change_form.html'

    form = MenuForm

    # remove a opcao de recuperar excluidos
    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.change_list_template = None

        return super(MenuAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(MenuAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)

        return ModelFormMetaClass

    def menu_pai(self, obj):
        if obj.parent is None:
            return "-------"
        return obj.parent
    menu_pai.short_description = u'Menu pai'

    def get_queryset(self, request):
        qs = super(MenuAdmin, self).get_queryset(request)
        return qs.filter(site__in=request.user.permissao.sites.all()).distinct()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "site":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(MenuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Menu, MenuAdmin)
