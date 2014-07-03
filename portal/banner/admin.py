#coding: utf-8
from django.contrib import admin
from portal.banner.models import Banner
# Register your models here.
from django.contrib.admin.options import ModelAdmin




class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'arquivo')
    search_fields = ('titulo', 'data_publicacao')
    date_hierarchy = 'data_publicacao'


admin.site.register(Banner, BannerAdmin)