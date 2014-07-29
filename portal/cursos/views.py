# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from portal.cursos.models import Curso, Grupo_Cursos
from django.http import HttpResponse # httresponse para usar com json
import json # json para usar no select com ajax

# Create your views here.


def jsoncampi(request, formacao_id):
    campi = Curso.objects.select_related('Campus').filter(formacao=formacao_id).values_list('campus__id', 'campus__nome').distinct()
    dados = dict(campi)
    return HttpResponse(json.dumps(dados), content_type="application/json")


def jsoncursos(request, formacao_id, campus_id):
    dados = dict(Curso.objects.select_related('Grupo_Cursos').filter(formacao=formacao_id, campus=campus_id).values_list('grupo__id', 'grupo__nome').distinct())
    return HttpResponse(json.dumps(dados), content_type="application/json")


def listagrupodecursos(request):
    formacao = Curso.objects.select_related('Formacao').values('formacao__id', 'formacao__nome').distinct()
    campi = Curso.objects.select_related('Campus').values('campus__id', 'formacao__id', 'campus__nome').distinct()
    grupo_cursos = Curso.objects.select_related('Grupo_Cursos').values('formacao__id', 'formacao__nome', 'campus__id', 'campus__nome', 'grupo__id', 'grupo__nome').distinct()
    return render(request, 'cursos/listagrupodecursos.html', {'formacao': formacao,'grupo_cursos': grupo_cursos, 'campi': campi})


def listacursosdogrupo(request, campus_id, grupo_id):
    grupo = get_object_or_404(Grupo_Cursos, id=grupo_id)
    cursos = Curso.objects.filter(campus=campus_id, grupo=grupo_id)
    return render(request, 'cursos/listacursos.html', {'grupo': grupo, 'cursos': cursos})


def exibecurso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'cursos/exibecurso.html', {'curso': curso})


def guiadecursoportal(request):
    if request.method == 'POST':
        if int(request.POST.get('campi')) > 0 and int(request.POST.get('cursos')) > 0:
            return listacursosdogrupo(request, request.POST.get('campi'), request.POST.get('cursos'))
        else:
            return listagrupodecursos(request)
    elif request.method == 'GET':
        return listagrupodecursos(request)
    else:
        return listagrupodecursos(request)