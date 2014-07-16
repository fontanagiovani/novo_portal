from django.contrib import admin
from portal.cursos.models import Campus, Curso, Formacao, Grupo_Cursos

# Register your models here.


class FormacaoAdmin(admin.ModelAdmin):
    pass


class CampusAdmin(admin.ModelAdmin):
    pass


class CursoAdmin(admin.ModelAdmin):
    pass


class Grupo_CursosAdmin(admin.ModelAdmin):
    pass


admin.site.register(Formacao, FormacaoAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Grupo_Cursos, Grupo_CursosAdmin)