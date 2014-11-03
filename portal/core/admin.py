# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils import timezone
import reversion

from portal.core.models import SiteDetalhe
from portal.core.models import Destino
from portal.core.models import Campus
from portal.core.models import ContadorVisitas
# from portal.core.models import Selecao, TipoSelecao

from portal.core.forms import SiteDetalheFormset


class SiteListFilter(admin.SimpleListFilter):
    # USAGE
    # list_filter = (CategoryListFilter,)

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Site(s)'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'sites__id__exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = []
        for site in request.user.permissao.sites.all():
            list_tuple.append((site.id, site.domain))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(site__id__exact=self.value())
        else:
            return queryset


class SitesListFilter(admin.SimpleListFilter):
    # USAGE
    # list_filter = (CategoryListFilter,)

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Site(s)'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'sites__id__exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = []
        for site in request.user.permissao.sites.all():
            list_tuple.append((site.id, site.domain))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(sites__id__exact=self.value())
        else:
            return queryset


class EstaPublicadoListFilter(admin.SimpleListFilter):
    # USAGE
    # list_filter = (CategoryListFilter,)

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Publicado'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'publicado__exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = list()
        list_tuple.append((1, u'Sim'))
        list_tuple.append((0, u'Não'))
        # for site in request.user.permissao.sites.all():
        #     list_tuple.append((site.id, site.domain))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            if self.value() == '0':
                return queryset.filter(Q(publicado=False) | Q(data_publicacao__gt=timezone.now()))
            else:
                return queryset.filter(publicado=True, data_publicacao__lte=timezone.now())
        else:
            return queryset


class ContemInativoListFilter(admin.SimpleListFilter):
    # USAGE
    # list_filter = (CategoryListFilter,)

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Inativo'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'domain__contains'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = list()
        list_tuple.append(('inativo', u'Inativos'))
        # list_tuple.append((0, u'Não'))
        # for site in request.user.permissao.sites.all():
        #     list_tuple.append((site.id, site.domain))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            if self.value():
                return queryset.filter(domain__contains='inativo')
        else:
            return queryset


class CampusAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    pass
    # list_display = ('nome', )
    # search_fields = ('nome',)

admin.site.register(Campus, CampusAdmin)


class SiteIndexInline(admin.StackedInline):
    model = SiteDetalhe
    formset = SiteDetalheFormset

    max_num = 1
    can_delete = False


class SiteIndexAdmin(reversion.VersionAdmin, SiteAdmin):
    list_filter = (ContemInativoListFilter, )
    inlines = [SiteIndexInline]

admin.site.unregister(Site)
admin.site.register(Site, SiteIndexAdmin)


class DestinoAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    pass

admin.site.register(Destino, DestinoAdmin)


class ContadorAdmin(admin.ModelAdmin):
    list_display = ('url', 'contagem')
    search_fields = ('url', )

admin.site.register(ContadorVisitas, ContadorAdmin)

# class TipoSelecaoAdmin(reversion.VersionAdmin, admin.ModelAdmin):
#     list_display = ('titulo', 'parent',)
#     search_fields = ('titulo',)
#     prepopulated_fields = {'slug': ('titulo',)}
#
# admin.site.register(TipoSelecao, TipoSelecaoAdmin)
#
#
# class SelecaoAdmin(reversion.VersionAdmin, admin.ModelAdmin):
#     list_display = ('titulo', 'tipo', 'status', 'data_abertura_edital', 'data_abertura_inscricoes',
#                     'data_encerramento_inscricoes', )
#     search_fields = ('titulo', 'tipo', 'status', 'data_abertura_edital', 'data_abertura_inscricoes',
#                      'data_encerramento_inscricoes', )
#     date_hierarchy = 'data_abertura_edital'
#     list_filter = ('status', 'tipo')
#
# admin.site.register(Selecao, SelecaoAdmin)
