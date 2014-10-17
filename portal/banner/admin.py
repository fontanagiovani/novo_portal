#coding: utf-8
from django.contrib import admin
from django.contrib.sites.models import Site
import reversion

from portal.core.admin import SitesListFilter, EstaPublicadoListFilter
from portal.banner.models import Banner
from portal.banner.forms import BannerForm


class BannerAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'data_publicacao', 'arquivo', 'get_publicacao')
    search_fields = ('titulo', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = (SitesListFilter, EstaPublicadoListFilter, 'tipo')

    form = BannerForm

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'titulo',
                'tipo',
                'url',
                'arquivo',
            )
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(BannerAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def get_queryset(self, request):
        qs = super(BannerAdmin, self).get_queryset(request)
        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(BannerAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Banner, BannerAdmin)
