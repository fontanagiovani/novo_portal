# coding: utf-8
from portal.banner.models import Banner, BannerAcessoRapido
from django.shortcuts import render
from portal.conteudo.models import Noticia, Evento, Video, Galeria
from portal.core.models import Selecao, TipoSelecao
from portal.cursos.models import Curso
from django.http import HttpResponse # httresponse para usar com json
import json # json para usar no select com ajax


def home(request):
    noticias_detaque = sorted(Noticia.objects.filter(destaque=True)[:5], key=lambda o: o.prioridade_destaque)
    mais_noticias = Noticia.objects.all().exclude(
        id__in=[obj.id for obj in noticias_detaque])[:10]
    eventos = Evento.objects.all()[:3]
    banners = Banner.objects.all()[:3]
    acesso_rapido = BannerAcessoRapido.objects.all()[:5]
    videos = Video.objects.all()[:1]
    galerias = Galeria.objects.all()[:3]
    formacao = Curso.objects.select_related('Formacao').values('formacao__id', 'formacao__nome').distinct()

    return render(request, 'core/portal.html', {
        'noticias_destaque': noticias_detaque,
        'mais_noticias': mais_noticias,
        'eventos': eventos,
        'banners': banners,
        'acesso_rapido': acesso_rapido,
        'videos': videos,
        'galerias': galerias,
        'formacao': formacao,
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

def jsoncampi(request, formacao_id):
    campi = Curso.objects.select_related('Campus').filter(formacao=formacao_id).values_list('campus__id', 'campus__nome').distinct()
    # dados = {'1': 'Cuiabá', '2': 'Campo Novo do Parecis'}
    dados = dict(campi)
    return HttpResponse(json.dumps(dados), content_type="application/json")


def jsoncursos(request, formacao_id, campus_id):
    dados = dict(Curso.objects.select_related('Grupo_Cursos').filter(formacao=formacao_id, campus=campus_id).values_list('grupo__id', 'grupo__nome').distinct())
    return HttpResponse(json.dumps(dados), content_type="application/json")