# coding: utf-8
from portal.banner.models import Banner
from django.shortcuts import render, get_object_or_404
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.conteudo.models import Video


def home(request):
    noticias_detaque = sorted(Noticia.objects.filter(destaque=True)[:5], key=lambda o: o.prioridade_destaque)

    mais_noticias = Noticia.objects.all().exclude(
        id__in=[obj.id for obj in noticias_detaque])[:9]

    eventos = Evento.objects.all()[:3]

    banners = Banner.objects.all()[:3]

    videos = Video.objects.all()[:1]

    return render(request, 'core/portal.html', {
        'noticias_destaque': noticias_detaque,
        'mais_noticias': mais_noticias,
        'eventos': eventos,
        'banners': banners,
        'videos': videos,
    })


def grid(request):
    noticias_detaque = sorted(Noticia.objects.filter(destaque=True)[:5], key=lambda o: o.prioridade_destaque)

    mais_noticias = Noticia.objects.all().exclude(
        id__in=[obj.id for obj in noticias_detaque])[:9]

    eventos = Evento.objects.all()[:3]

    banners = Banner.objects.all()[:3]

    videos = Video.objects.all()[:1]

    return render(request, 'core/portal.html', {
        'noticias_destaque': noticias_detaque,
        'mais_noticias': mais_noticias,
        'eventos': eventos,
        'banners': banners,
        'videos': videos,
    })

# def conteudo_detalhe(request, conteudo_id):
#     conteudo = get_object_or_404(Conteudo, id=conteudo_id)
#
#     return render(request, 'core/conteudo.html', {'conteudo': conteudo})

# def exemplo_form_admin(request):
#     return render(request, 'core/exemplo_form_admin.html', {'form': SiteForm()})


# def thumbnail(request, conteudo_id):
#     conteudo = get_object_or_404(Conteudo, pk=conteudo_id)
#     return render(request, 'core/thumbnail.html', {'conteudo': conteudo})
