# -*- coding: utf-8 -*-
from django.contrib import admin
from portal.cursos.models import Campus, Curso, Formacao, GrupoCursos


class FormacaoAdmin(admin.ModelAdmin):
    pass


class CampusAdmin(admin.ModelAdmin):
    pass


class CursoAdmin(admin.ModelAdmin):
    pass


class GrupoCursosAdmin(admin.ModelAdmin):
    pass


admin.site.register(Formacao, FormacaoAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(GrupoCursos, GrupoCursosAdmin)