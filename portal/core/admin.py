# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.core.models import Pagina
from portal.core.models import MidiaPagina



class MidiaPaginaInLine(admin.StackedInline):
    model = MidiaPagina
    extra = 1


class PaginaAdmin(SummernoteModelAdmin):
    inlines = (MidiaPaginaInLine, )

admin.site.register(Pagina, PaginaAdmin)