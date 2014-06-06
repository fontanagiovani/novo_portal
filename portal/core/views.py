# coding: utf-8
from portal.core.models import Conteudo
from django.shortcuts import render, get_object_or_404


def home(request):
    noticias = Conteudo.objects.filter(tipo='NOTICIAS')[:8]
    eventos = Conteudo.objects.filter(tipo='EVENTOS')[:3]
    banners = Conteudo.objects.filter(tipo='BANNER')[:3]
    return render(request, 'core/portal.html', {'noticias': noticias, 'eventos': eventos, 'banners': banners})


# def exemplo_form_admin(request):
#     return render(request, 'core/exemplo_form_admin.html', {'form': SiteForm()})



def thumbnail(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, pk=conteudo_id)
    return render (request, 'core/thumbnail.html', {'conteudo': conteudo})