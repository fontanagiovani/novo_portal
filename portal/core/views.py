# coding: utf-8
from portal.banner.models import Banner, BannerAcessoRapido
from django.shortcuts import render
from portal.conteudo.models import Noticia, Evento, Video, Galeria
from portal.core.models import Selecao, TipoSelecao


def home(request):
    noticias_detaque = sorted(Noticia.objects.filter(destaque=True)[:5], key=lambda o: o.prioridade_destaque)

    mais_noticias = Noticia.objects.all().exclude(
        id__in=[obj.id for obj in noticias_detaque])[:10]

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
        'galerias': galerias,
    })


def selecao(request):
    lista = Selecao.objects.all()
    menu = TipoSelecao.objects.all()

    titulo = 0
    tipo = request.GET.get('tipo')
    status = request.GET.get('status')
    ano = request.GET.get('ano')

    if tipo:
        lista = lista.filter(tipo=tipo)
        titulo = menu.get(id=tipo)
        tipo = 'tipo=' + tipo + '&'
    else:
        tipo = ''

    if status:
        lista = lista.filter(status=status)
        status = 'status=' + status + '&'
    else:
        status = ''

    if ano:
        lista = lista.filter(data_abertura_edital__year=ano)
        ano = 'ano=' + ano
        # if tipo or status :
        #     ano = '&' + ano
    else:
        # ano = datetime.date.today().year
        ano = ''

    return render(request, 'core/selecao_lista.html', {
        'lista': lista,
        'ano': ano,
        'status': status,
        'tipo': tipo,
        'nodes': menu,
        'titulo': titulo
    })
