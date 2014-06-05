# coding: utf-8
from portal.core.models import Conteudo
from django.shortcuts import render, get_object_or_404


def home(request):
    noticias_detaque = Conteudo.objects.filter(destaque=True)[:5]
    mais_noticias = Conteudo.objects.exclude(id__in=noticias_detaque.values_list('id', flat=True))[:8]
    return render(request, 'core/portal.html', {
        'noticias_destaque': noticias_detaque,
        'mais_noticias': mais_noticias}
    )

# def exemplo_form_admin(request):
#     return render(request, 'core/exemplo_form_admin.html', {'form': SiteForm()})

def thumbnail(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, pk=conteudo_id)
    return render (request, 'core/thumbnail.html', {'conteudo': conteudo})