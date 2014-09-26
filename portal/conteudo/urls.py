# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('portal.conteudo.views',
                       # Noticias
                       url(r'^noticia/(?P<slug>[\w_-]+)/$', 'noticia_detalhe', name='noticia_detalhe'),
                       url(r'^noticia/preview/(?P<slug>[\w_-]+)/$', 'noticia_detalhe_preview',
                           name='noticia_detalhe_preview'),
                       url(r'^noticias/$', 'noticias_lista', name='noticias_lista'),

                       # Paginas
                       url(r'^pagina/(?P<slug>[\w_-]+)/$', 'pagina_detalhe', name='pagina_detalhe'),
                       url(r'^pagina/preview/(?P<slug>[\w_-]+)/$', 'pagina_detalhe_preview',
                           name='pagina_detalhe_preview'),

                       # Eventos
                       url(r'^evento/(?P<slug>[\w_-]+)/$', 'evento_detalhe', name='evento_detalhe'),
                       url(r'^evento/preview/(?P<slug>[\w_-]+)/$', 'evento_detalhe_preview',
                           name='evento_detalhe_preview'),
                       url(r'^eventos/$', 'eventos_lista', name='eventos_lista'),

                       # Videos
                       url(r'^video/(?P<slug>[\w_-]+)/$', 'video_detalhe', name='video_detalhe'),
                       url(r'^video/preview/(?P<slug>[\w_-]+)/$', 'video_detalhe_preview',
                           name='video_detalhe_preview'),
                       url(r'^videos/$', 'videos_lista', name='videos_lista'),

                       # Galerias
                       url(r'^galeria/(?P<slug>[\w_-]+)/$', 'galeria_detalhe', name='galeria_detalhe'),
                       url(r'^galeria/preview/(?P<slug>[\w_-]+)/$', 'galeria_detalhe_preview',
                           name='galeria_detalhe_preview'),
                       url(r'^galerias/$', 'galerias_lista', name='galerias_lista'),

                       # Tags
                       url(r'^tag/(?P<slug>[\w_-]+)/$', 'tags_lista', name='tags_lista'),

                       # Licitação
                       url(r'^licitacao/(?P<licitacao_id>\d+)/$', 'licitacao_detalhe', name='licitacao_detalhe'),
                       url(r'^licitacoes/$', 'licitacoes', name='licitacoes_modalidades'),
                       url(r'^licitacoes/(?P<modalidade>\d+)/$', 'licitacoes', name='licitacoes_lista'),
                       url(r'^licitacoes/(?P<modalidade>\d+)/(?P<ano>\d+)/$', 'licitacoes', name='licitacoes_ano'),
                       )