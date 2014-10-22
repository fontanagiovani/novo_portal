# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
from django.http.response import Http404
from django.utils import timezone
from pure_pagination import Paginator, PageNotAnInteger
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
        noticia = Noticia.publicados.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Noticia.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/noticia.html', {'noticia': noticia})


@login_required
def noticia_detalhe_preview(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        noticia = Noticia.objects.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Noticia.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/noticia.html', {'noticia': noticia})


def noticias_lista(request):
    try:
        page = request.GET.get('page', 1)

    except PageNotAnInteger:
        page = 1

    try:
        site = Site.objects.get(domain=request.get_host())
        objects = Noticia.publicados.filter(sites__id__exact=site.id)
        paginator = Paginator(objects, request=request, per_page=25)
        noticias = paginator.page(page)

    except Site.DoesNotExist, Noticia.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/noticias_lista.html', {'noticias': noticias})


def pagina_detalhe(request, slug):
    try:
        pagina = Pagina.publicados.get(slug=slug)
    except Pagina.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/pagina.html', {'pagina': pagina})


@login_required
def pagina_detalhe_preview(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        pagina = Pagina.objects.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Pagina.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/pagina.html', {'pagina': pagina})


def evento_detalhe(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        evento = Evento.publicados.get(slug=slug, sites__id__exact=site.id)
    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404
    return render(request, 'conteudo/evento.html', {'evento': evento})


@login_required
def evento_detalhe_preview(request, slug):
    try:
        site = Site.objects.get(domain=request.get_host())
        evento = Evento.objects.get(slug=slug, sites__id__exact=site.id)

    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404
    return render(request, 'conteudo/evento.html', {'evento': evento})


def eventos_lista(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    try:
        site = Site.objects.get(domain=request.get_host())
        objects = Evento.publicados.filter(sites__id__exact=site.id)
        paginator = Paginator(objects, request=request, per_page=25)
        eventos = paginator.page(page)

    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/eventos_lista.html', {'eventos': eventos})


def video_detalhe(request, slug):
    try:
        video = Video.publicados.get(slug=slug)

    except Video.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/video.html', {'video': video})


@login_required
def video_detalhe_preview(request, slug):
    video = get_object_or_404(Video, slug=slug)

    return render(request, 'conteudo/video.html', {'video': video})


def videos_lista(request):
    try:
        page = request.GET.get('page', 1)

    except PageNotAnInteger:
        page = 1

    try:
        site = Site.objects.get(domain=request.get_host())
        objects = Video.publicados.filter(sites__id__exact=site.id)
        paginator = Paginator(objects, request=request, per_page=25)
        videos = paginator.page(page)

    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/videos_lista.html', {'videos': videos})


def galeria_detalhe(request, slug):
    try:
        galeria = Galeria.publicados.get(slug=slug)

    except Site.DoesNotExist, Video.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/galeria.html', {'galeria': galeria})


@login_required
def galeria_detalhe_preview(request, slug):
    galeria = get_object_or_404(Galeria, slug=slug)

    return render(request, 'conteudo/galeria.html', {'galeria': galeria})


def galerias_lista(request):
    try:
        page = request.GET.get('page', 1)

    except PageNotAnInteger:
        page = 1

    try:
        site = Site.objects.get(domain=request.get_host())
        objects = Galeria.publicados.filter(sites__id__exact=site.id)
        paginator = Paginator(objects, request=request, per_page=25)
        galerias = paginator.page(page)

    except Site.DoesNotExist, Evento.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/galerias_lista.html', {'galerias': galerias})


def tags_lista(request, slug):
    try:
        page = request.GET.get('page', 1)

    except PageNotAnInteger:
        page = 1

    try:
        site = Site.objects.get(domain=request.get_host())

        # trecho utilizado para restringir a exibicao de objetos ao site atual
        objects = TaggedItem.objects.filter(tag__slug__iexact=slug)
        itens = []

        for i in objects:
            if site in i.content_object.sites.all():
                itens.append(i)

        paginator = Paginator(itens, request=request, per_page=25)
        tags = paginator.page(page)

    except Site.DoesNotExist, TaggedItem.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/tag_lista.html', {'tags': tags, 'slug': slug})


def licitacao_detalhe(request, licitacao_id):
    try:
        site = Site.objects.get(domain=request.get_host())
        licitacao = Licitacao.publicados.get(id=licitacao_id, sites__id__exact=site.id)
    except Site.DoesNotExist, Licitacao.DoesNotExist:
        raise Http404

    return render(request, 'conteudo/licitacao.html', {'licitacao': licitacao})


def licitacoes_lista(request, modalidade=None, ano=None):

    if modalidade:
        try:
            page = request.GET.get('page', 1)

        except PageNotAnInteger:
            page = 1
        try:
            site = Site.objects.get(domain=request.get_host())
            modalidade = modalidade

            if not ano:
                ano = str(timezone.now().year)

            objects = Licitacao.publicados.filter(sites__id__exact=site.id, modalidade=modalidade,
                                                  data_publicacao__year=ano)
            paginator = Paginator(objects, request=request, per_page=25)
            licitacoes = paginator.page(page)

        except Site.DoesNotExist, Licitacao.DoesNotExist:
            raise Http404

        anos = Licitacao.publicados.filter().datetimes('data_publicacao', 'year', order='DESC')

        return render(request, 'conteudo/licitacoes_lista.html', {'licitacoes': licitacoes, 'anos': anos, 'ano': ano,
                                                                  'modalidade': modalidade})
    else:
        site = Site.objects.get(domain=request.get_host())
        modalidades = Licitacao.get_modalidades_existentes(site)

        return render(request, 'conteudo/licitacoes_modalidades.html', {'modalidades': modalidades})
