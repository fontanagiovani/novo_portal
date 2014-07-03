from django.shortcuts import render
from portal.cursos.models import Curso, Campus, Grupo_Cursos, Formacao

# Create your views here.

def listatudo(request):
    # grupo  = Grupo_Cursos.objects.distinct('formacao')
    grupo  = Grupo_Cursos.objects.all()
    return render(request, 'cursos/listacursos.html', {'grupo': grupo,})