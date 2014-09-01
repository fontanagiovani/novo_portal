#coding: utf-8
from django.contrib import admin
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from portal.banner.forms import BannerForm
from portal.banner.forms import BannerAcessoRapidoForm


class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'arquivo')
    search_fields = ('titulo', 'data_publicacao')
    date_hierarchy = 'data_publicacao'

    form = BannerForm

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(BannerAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass


class BannerAcessoRapidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'midia_image')
    search_fields = ('titulo', 'data_publicacao')
    date_hierarchy = 'data_publicacao'

    form = BannerAcessoRapidoForm

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(BannerAcessoRapidoAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass


admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerAcessoRapido, BannerAcessoRapidoAdmin)