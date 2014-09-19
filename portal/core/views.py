# coding: utf-8
from collections import OrderedDict
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect
from django.http import HttpResponse  # httresponse para usar com json
from django.http.response import Http404
import json  # json para usar no select com ajax
from haystack.views import SearchView

from portal.core.models import Menu
from portal.core.models import Template
from portal.core.models import Selecao, TipoSelecao
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from portal.cursos.models import Curso


def home(request):
    contexto = dict()
    try:
        site = Site.objects.get(domain=request.get_host())

        if site.sitedetalhe.template.descricao == Template.redirect():
            return redirect(site.sitedetalhe.template.caminho)

        if site.sitedetalhe.template.descricao == Template.portal():
            noticias_detaque = sorted(Noticia.objects.filter(destaque=True, sites__id__exact=site.id)[:5],
                                      key=lambda o: o.prioridade_destaque)
            mais_noticias = Noticia.objects.filter(sites__id__exact=site.id).exclude(
                id__in=[obj.id for obj in noticias_detaque])[:10]
            eventos = Evento.objects.filter(sites__id__exact=site.id)[:3]
            banners = Banner.objects.filter(sites__id__exact=site.id)[:3]
            acesso_rapido = BannerAcessoRapido.objects.filter(sites__id__exact=site.id)[:5]
            videos = Video.objects.filter(sites__id__exact=site.id)[:1]
            galerias = Galeria.objects.filter(sites__id__exact=site.id)[:3]
            formacao = Curso.objects.select_related('Formacao').values('formacao__id', 'formacao__nome').distinct()

            contexto = {
                'noticias_destaque': noticias_detaque,
                'mais_noticias': mais_noticias,
                'eventos': eventos,
                'banners': banners,
                'acesso_rapido': acesso_rapido,
                'videos': videos,
                'galerias': galerias,
                'formacao': formacao,
            }
        if site.sitedetalhe.template.descricao == Template.blog():
            noticias = Noticia.objects.all()[:10]

            contexto = {
                'noticias': noticias,
            }

        # Adiconar o contexto para os demais tipos de template nos demais condicionais

    except (Site.DoesNotExist, Noticia.DoesNotExist, Evento.DoesNotExist,
            Banner.DoesNotExist, BannerAcessoRapido.DoesNotExist, Video.DoesNotExist,
            Galeria.DoesNotExist):
        raise Http404

    contexto['site'] = site

    return render(request, site.sitedetalhe.template.caminho, contexto)


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
    else:
        ano = ''

    return render(request, 'core/selecao_lista.html', {
        'lista': lista,
        'ano': ano,
        'status': status,
        'tipo': tipo,
        'nodes': menu,
        'titulo': titulo
    })


def json_campi(request, formacao_id):
    campi = Curso.objects.select_related('Campus').filter(
        formacao=formacao_id).values_list('campus__id', 'campus__nome').distinct()
    dados = dict(campi)
    return HttpResponse(json.dumps(dados), content_type="application/json")


def json_cursos(request, formacao_id, campus_id):
    dados = dict(Curso.objects.select_related('GrupoCursos').filter(
        formacao=formacao_id, campus=campus_id).values_list('grupo__id', 'grupo__nome').distinct())
    return HttpResponse(json.dumps(dados), content_type="application/json")


def admin_site_menu(request, site_id):
    try:
        site = Site.objects.get(id=site_id)
    except Site.DoesNotExist:
        raise Http404
    menus = Menu.objects.filter(site=site)

    return HttpResponse(json.dumps(serialize_menus(menus)), mimetype="application/json")


def serialize_menus(queryset):
    lista = []
    for menu in queryset:
        d = OrderedDict()
        d["ordem"] = menu.ordem
        d["id"] = menu.id
        d["titulo"] = '---' * menu.get_level() + ' ' + menu.titulo
        lista.append(d)
    return lista


class SearchViewSites(SearchView):
    # sobrescrita do metodo para filtar pelo dominio da requisicao
    def get_results(self):
        results = super(SearchViewSites, self).get_results()
        results = results.filter(text__contains=self.request.get_host())

        # import ipdb
        # ipdb.set_trace()
        return results