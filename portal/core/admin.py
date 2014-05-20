# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from portal.core.models import Curso
from portal.core.models import Site
from portal.core.models import Menu
from portal.core.models import MenuContainer
from portal.core.models import Pagina
from portal.core.models import Midia


class CursoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Curso, CursoAdmin)


class SiteAdmin(MPTTModelAdmin):
    pass

admin.site.register(Site, SiteAdmin)


class MenuAdmin(admin.ModelAdmin):
    pass

admin.site.register(Menu, MenuAdmin)


class MenuContainerAdmin(admin.ModelAdmin):
    pass

admin.site.register(MenuContainer, MenuContainerAdmin)


class MidiaInLine(admin.StackedInline):
    model = Midia
    extra = 1


class PaginaAdmin(SummernoteModelAdmin):
    inlines = (MidiaInLine, )

admin.site.register(Pagina, PaginaAdmin)