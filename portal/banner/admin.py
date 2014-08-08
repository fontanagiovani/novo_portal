#coding: utf-8
from django.contrib import admin
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido


class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'arquivo')
    search_fields = ('titulo', 'data_publicacao')
    date_hierarchy = 'data_publicacao'


class BannerAcessoRapidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'midia_image')
    search_fields = ('titulo', 'data_publicacao')
    date_hierarchy = 'data_publicacao'


admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerAcessoRapido, BannerAcessoRapidoAdmin)