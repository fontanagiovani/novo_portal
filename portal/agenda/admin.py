# -*- coding: utf-8 -*-
from django.contrib import admin
from portal.agenda.models import Agenda
from django.db.models import CharField # usado pelo formfield_overrides
from django.forms import TextInput # usado pelo formfield_overrides

# Register your models here.

class AgendaAdmin(admin.ModelAdmin):
    fields = ('descricao', 'inicio', 'fim', 'local',)
    list_display = ('descricao', 'inicio', 'fim',)
    list_filter = ('inicio', 'fim')
    date_hierarchy = 'inicio'
    search_fields = ('descricao',)

    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': '85'})},
        # from django.forms import Textarea
        # TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

admin.site.register(Agenda, AgendaAdmin)
