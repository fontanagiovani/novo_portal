# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from portal.core.models import Curso
from portal.core.models import Site
from portal.core.models import Menu
from portal.core.models import MenuContainer
from portal.core.models import Pagina
from portal.core.models import MidiaPagina


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
    model = MidiaPagina
    extra = 0


class PaginaAdmin(admin.ModelAdmin):
    inlines = (MidiaInLine, )

admin.site.register(Pagina, PaginaAdmin)