# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
from django.http.response import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import TaggedItem

from portal.conteudo.models import Noticia
from portal.conteudo.models import Pagina
from portal.conteudo.models import Evento
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria
from portal.conteudo.models import Licitacao


def noticia_detalhe(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        noticia = Noticia.objects.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Noticia.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/noticia.html', {'noticia': noticia})


def noticias_lista(request):
    try:
        site = Site.objects.get(domain=request.get_host())
        paginator = Paginator(Noticia.objects.filter(sites__id__exact=site.id), 20)
    except Site.DoesNotExist, Noticia.DoesNotExist:
        raise Http404

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


def pagina_detalhe(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        pagina = Pagina.objects.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Pagina.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/pagina.html', {'pagina': pagina})


def evento_detalhe(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        evento = Evento.objects.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/evento.html', {'evento': evento})


def eventos_lista(request):
    try:
        site = Site.objects.get(domain=request.get_host())
        paginator = Paginator(Evento.objects.filter(sites__id__exact=site.id), 20)
    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

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


def video_detalhe(request, slug):
    video = get_object_or_404(Video, slug=slug)

    return render(request, 'conteudo/video.html', {'video': video})


def videos_lista(request):
    try:
        site = Site.objects.get(domain=request.get_host())
        paginator = Paginator(Video.objects.filter(sites__id__exact=site.id), 20)
    except Site.DoesNotExist, Video.DoesNotExist:
        raise Http404

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


def galeria_detalhe(request, slug):
    galeria = get_object_or_404(Galeria, slug=slug)

    return render(request, 'conteudo/galeria.html', {'galeria': galeria})


def galerias_lista(request):
    try:
        site = Site.objects.get(domain=request.get_host())
        paginator = Paginator(Galeria.objects.filter(sites__id__exact=site.id), 20)
    except Site.DoesNotExist, Galeria.DoesNotExist:
        raise Http404

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


def tags_lista(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())

        # trecho utilizado para restringir a exibicao de objetos ao site atual
        tags = TaggedItem.objects.filter(tag__slug__iexact=slug)
        itens = []

        for i in tags:
            if site in i.content_object.sites.all():
                itens.append(i)

        paginator = Paginator(itens, 20)
    except Site.DoesNotExist, TaggedItem.DoesNotExist:
        raise Http404

    page = request.GET.get('page')
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tags = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tags = paginator.page(paginator.num_pages)

    return render(request, 'conteudo/tag_lista.html', {'tags': tags, 'slug': slug})


def licitacao_detalhe(request, licitacao_id):
    try:
        site = Site.objects.get(domain=request.get_host())
        licitacao = Licitacao.objects.get(id=licitacao_id, sites__id__exact=site.id)
    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/licitacao.html', {'licitacao': licitacao})


def licitacoes_lista(request):
    try:
        site = Site.objects.get(domain=request.get_host())
        paginator = Paginator(Licitacao.objects.filter(sites__id__exact=site.id), 20)
    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

    page = request.GET.get('page')
    try:
        licitacoes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        licitacoes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        licitacoes = paginator.page(paginator.num_pages)
    #
    return render(request, 'conteudo/licitacoes_lista.html', {'licitacoes': licitacoes})