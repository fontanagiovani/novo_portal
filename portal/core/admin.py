# -*- coding: utf-8 -*-
from django.contrib import admin
from portal.core.models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('titulo','parent')
    search_fields = ('titulo',)
    prepopulated_fields = {'slug':('titulo',)}

admin.site.register(Menu,MenuAdmin)