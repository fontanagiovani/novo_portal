# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from portal.cursos.models import Curso, GrupoCursos
from django.http import HttpResponse  # httresponse para usar com json
import json  # json para usar no select com ajax


def listadedicionarios(queryset):
    lista = []
    for l in queryset:
        d = dict()
        d["formacao_id"] = l[0]
        d["formacao_nome"] = l[1]
        d["campus_id"] = l[2]
        d["campus_nome"] = l[3]
        d["grupo_id"] = l[4]
        d["grupo_nome"] = l[5]
        d["grupo_url"] = GrupoCursos.objects.get(pk=l[4]).get_absolute_url()
        lista.append(d)
    return lista


def jsonformacao(request, formacao_id):
    queryset = Curso.objects.select_related().filter(formacao=formacao_id).values_list(
        'formacao__id', 'formacao__nome', 'campus__id', 'campus__nome', 'grupo__id', 'grupo__nome'
    ).distinct()
    dados = listadedicionarios(queryset)
    return HttpResponse(json.dumps(dados), mimetype="application/json")


def jsoncampi(request, campus_id):
    queryset = Curso.objects.select_related().filter(campus=campus_id).values_list(
        'formacao__id', 'formacao__nome', 'campus__id', 'campus__nome', 'grupo__id', 'grupo__nome'
    ).distinct()
    dados = listadedicionarios(queryset)
    return HttpResponse(json.dumps(dados), mimetype="application/json")


def jsoncursos(request, curso_id):
    queryset = Curso.objects.select_related().filter(grupo=curso_id).values_list(
        'formacao__id', 'formacao__nome', 'campus__id', 'campus__nome', 'grupo__id', 'grupo__nome'
    ).distinct()
    dados = listadedicionarios(queryset)
    return HttpResponse(json.dumps(dados), mimetype="application/json")


def listagrupodecursos(request):
    formacao = Curso.objects.select_related('Formacao').values('formacao__id', 'formacao__nome').distinct()
    campi = Curso.objects.select_related('Campus').values('campus__id', 'formacao__id', 'campus__nome').distinct()
    grupo_cursos = Curso.objects.select_related('GrupoCursos').values('grupo__id', 'grupo__nome').distinct()

    return render(
        request, 'cursos/listagrupodecursos.html',
        {
            'formacao': formacao,
            'grupo_cursos': grupo_cursos,
            'campi': campi
        }
    )


def listacursosdogrupo(request, grupo_id):
    grupo = get_object_or_404(GrupoCursos, id=grupo_id)
    cursos = Curso.objects.select_related('Campus').filter(grupo=grupo_id)
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