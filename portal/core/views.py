# coding: utf-8
from portal.banner.models import Banner, BannerAcessoRapido
from django.shortcuts import render, get_object_or_404
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria
from portal.core.models import Selecao


def home(request):
    noticias_detaque = sorted(Noticia.objects.filter(destaque=True)[:5], key=lambda o: o.prioridade_destaque)

    mais_noticias = Noticia.objects.all().exclude(
        id__in=[obj.id for obj in noticias_detaque])[:9]

    eventos = Evento.objects.all()[:3]

    banners = Banner.objects.all()[:3]

    acesso_rapido = BannerAcessoRapido.objects.all()[:5]

    videos = Video.objects.all()[:1]

    galerias = Galeria.objects.all()[:3]


    return render(request, 'core/portal.html', {
        'noticias_destaque': noticias_detaque,
        'mais_noticias': mais_noticias,
        'eventos': eventos,
        'banners': banners,
        'acesso_rapido': acesso_rapido,
        'videos': videos,
        'galerias':galerias,
    })

def selecao(request):
    lista = Selecao.objects.all()

    tipo = request.GET.get('tipo')
    status = request.GET.get('status')
    ano = request.GET.get('ano')

    if tipo:
        lista = lista.filter(tipo=tipo)
    if status:
        lista = lista.filter(status=status)
    if ano:
        lista = lista.filter(data_abertura_edital__year=ano)

    return render(request, 'core/lista_selecao.html',{'lista':lista})

# def conteudo_detalhe(request, conteudo_id):
#     conteudo = get_object_or_404(Conteudo, id=conteudo_id)
#
#     return render(request, 'core/conteudo.html', {'conteudo': conteudo})

# def exemplo_form_admin(request):
#     return render(request, 'core/exemplo_form_admin.html', {'form': SiteForm()})


# def thumbnail(request, conteudo_id):
#     conteudo = get_object_or_404(Conteudo, pk=conteudo_id)
#     return render(request, 'core/thumbnail.html', {'conteudo': conteudo})
