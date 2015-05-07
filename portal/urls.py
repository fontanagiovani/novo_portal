# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from portal.core.views import SearchViewSites

sqs = SearchQuerySet().order_by('-data_publicacao')

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
                       url(r'^conteudo/', include('portal.conteudo.urls', namespace='conteudo')),
                       url(r'^selecao/', 'portal.core.views.selecao', name='selecao'),
                       url(r'^admin_site_menu/(?P<site_id>\d+)/$', 'portal.core.views.admin_site_menu',
                           name='admin_site_menu'),


                       url(r'buscar/$', search_view_factory(
                           view_class=SearchViewSites,
                           template='search/search.html',
                           searchqueryset=sqs,
                           form_class=ModelSearchForm
                       ), name='buscar'),

                       # url(r'^guiadecursos/', 'portal.cursos.views.listagrupodecursos', name='listagrupodecursos'),
                       url(r'^cursos/(?P<slug>[\w_-]+)/$', 'portal.cursos.views.listacursosdogrupo',
                           name='listacursosdogrupo'),
                       url(r'^curso/(?P<slug>[\w_-]+)/$', 'portal.cursos.views.exibecurso', name='exibecurso'),
                       url(r'^guiadecursoportal/', 'portal.cursos.views.guiadecursoportal', name='guiadecursoportal'),
                       url(r'^jsonformacao/(?P<formacao_id>\d+)/$', 'portal.cursos.views.jsonformacao',
                           name='jsonformacao'),
                       url(r'^jsoncampi/(?P<campus_id>\d+)/$', 'portal.cursos.views.jsoncampi', name='jsoncampi'),
                       url(r'^jsoncursos/(?P<curso_id>\d+)/$', 'portal.cursos.views.jsoncursos', name='jsoncursos'),
                       url(r'^json_campi/(?P<formacao_id>\d+)/$', 'portal.core.views.json_campi', name='json_campi'),
                       url(r'^json_cursos/(?P<formacao_id>\d+)/(?P<campus_id>\d+)/$', 'portal.core.views.json_cursos',
                           name='json_cursos'),

                       # urls de redirecionamento do antigoportal
                       url(r'^noticias/', 'portal.core.views.redirecionar_antigoportal', name='antigo_noticias'),
                       # url(r'^noticias/(?P<id_noticia>\d+)/$', 'portal.core.views.redirecionar_antigoportal'),
                       url(r'^licitacoes/', 'portal.core.views.redirecionar_antigoportal'),
                       # url(r'^licitacoes/(?P<id_modalidade>\d+)/$', 'portal.core.views.redirecionar_antigoportal'),
                       # url(r'^licitacoes/(?P<id_modalidade>\d+)/(?P<id_licitacao>\d+)/$', 'portal.core.views.redirecionar_antigoportal'),
                       url(r'^post/', 'portal.core.views.redirecionar_antigoportal'),
                       url(r'^get_file/', 'portal.core.views.redirecionar_antigoportal'),
                       url(r'^get_file_from_name/', 'portal.core.views.redirecionar_antigoportal'),
                       url(r'^pesquisar/', 'portal.core.views.redirecionar_antigoportal'),
                       # fim do redirecionamento de urls do antigoportal


                       url(r'^inicio/$', 'portal.core.views.home', name='home'),
                       url(r'^$', 'portal.core.views.hotsite', name='hotsite'),
                       )

# Trecho utilizado para que o django sirva os arquivos do diretorio media
from django.conf import settings

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))
