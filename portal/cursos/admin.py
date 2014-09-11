# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.cursos.models import Curso
from portal.cursos.models import Formacao
from portal.cursos.models import GrupoCursos
from portal.cursos.models import AnexoCurso


class FormacaoAdmin(admin.ModelAdmin):
    pass


class AnexoCursoInLine(admin.StackedInline):
    from django.forms import TextInput, Textarea
    from django.db import models
    model = AnexoCurso
    extra = 1

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'115'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

class CursoAdmin(SummernoteModelAdmin):
    inlines = [AnexoCursoInLine,]


class GrupoCursosAdmin(SummernoteModelAdmin):
    pass


admin.site.register(Formacao, FormacaoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(GrupoCursos, GrupoCursosAdmin)