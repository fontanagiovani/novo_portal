# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# from portal.cursos.models import Campus
from portal.cursos.models import Curso
from portal.cursos.models import Formacao
from portal.cursos.models import GrupoCursos


class FormacaoAdmin(admin.ModelAdmin):
    pass


# class CampusAdmin(admin.ModelAdmin):
#     pass


class CursoAdmin(admin.ModelAdmin):
    pass


class GrupoCursosAdmin(SummernoteModelAdmin):
    pass


admin.site.register(Formacao, FormacaoAdmin)
# admin.site.register(Campus, CampusAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(GrupoCursos, GrupoCursosAdmin)