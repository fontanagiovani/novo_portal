from django.shortcuts import render
from portal.cursos.models import Curso, Campus, Grupo_Cursos, Formacao

# Create your views here.


def listatudo(request):
    formacao = Curso.objects.select_related('Formacao').values('formacao__id', 'formacao__nome').distinct()
    campi = Curso.objects.select_related('Campus').values('campus__id', 'campus__nome').distinct()
    # grupo_cursos = Curso.objects.select_related('Grupo_Cursos').filter(formacao__nome__in=formacao).values('grupo__id', 'grupo__nome').distinct()
    grupo_cursos = Curso.objects.select_related('Grupo_Cursos').values('formacao__id', 'campus__id', 'grupo__nome').distinct()
    return render(request, 'cursos/listacursos.html', {'formacao': formacao,'grupo_cursos': grupo_cursos, 'campi': campi})