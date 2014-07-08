# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from portal.conteudo.models import Noticia
from portal.conteudo.models import Pagina
from portal.conteudo.models import Evento
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria



def noticia_detalhe(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)

    return render(request, 'conteudo/noticia.html', {'noticia': noticia})


def noticias_lista(request):
    paginator = Paginator(Noticia.objects.all(), 20)

    page = request.GET.get('page')
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        noticias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        noticias = paginator.page(paginator.num_pages)

    return render(request, 'conteudo/noticias_lista.html', {'noticias': noticias})


def pagina_detalhe(request, pagina_id):
    pagina = get_object_or_404(Pagina, id=pagina_id)

    return render(request, 'conteudo/pagina.html', {'pagina': pagina})


def evento_detalhe(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    return render(request, 'conteudo/evento.html', {'evento': evento})


def eventos_lista(request):
    paginator = Paginator(Evento.objects.all(), 20)

    page = request.GET.get('page')
    try:
        eventos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        eventos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        eventos = paginator.page(paginator.num_pages)

    return render(request, 'conteudo/eventos_lista.html', {'eventos': eventos})

def video_detalhe(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    return render(request, 'conteudo/video.html', {'video': video})


def videos_lista(request):
    paginator = Paginator(Video.objects.all(), 20)

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    return render(request, 'conteudo/videos_lista.html', {'videos': videos})


def galeria_detalhe(request, galeria_id):
    galeria = get_object_or_404(Galeria, id=galeria_id)

    return render(request, 'conteudo/galeria.html', {'galeria': galeria})


def galerias_lista(request):
    paginator = Paginator(Galeria.objects.all(), 20)

    page = request.GET.get('page')
    try:
        galerias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        galerias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        galerias = paginator.page(paginator.num_pages)

    return render(request, 'conteudo/galerias_lista.html', {'galerias': galerias})