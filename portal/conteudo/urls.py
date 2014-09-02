# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('portal.conteudo.views',
                       # Noticias
                       url(r'^noticia/(?P<noticia_id>\d+)/$', 'noticia_detalhe', name='noticia_detalhe'),
                       url(r'^noticias/$', 'noticias_lista', name='noticias_lista'),

                       # Paginas
                       url(r'^pagina/(?P<pagina_id>\d+)/$', 'pagina_detalhe', name='pagina_detalhe'),

                       # Eventos
                       url(r'^evento/(?P<evento_id>\d+)/$', 'evento_detalhe', name='evento_detalhe'),
                       url(r'^eventos/$', 'eventos_lista', name='eventos_lista'),

                       # Videos
                       url(r'^video/(?P<video_id>\d+)/$', 'video_detalhe', name='video_detalhe'),
                       url(r'^videos/$', 'videos_lista', name='videos_lista'),

                       # Galerias
                       url(r'^galeria/(?P<galeria_id>\d+)/$', 'galeria_detalhe', name='galeria_detalhe'),
                       url(r'^galerias/$', 'galerias_lista', name='galerias_lista'),

                       # Tags
                       url(r'^tag/(?P<tag_slug>[-\w]+)/$', 'tags_lista', name='tags_lista'),

                       # Licitação
                       url(r'^licitacao/(?P<licitacao_id>\d+)/$', 'licitacao_detalhe', name='licitacao_detalhe'),
                       url(r'^licitacoes/$', 'licitacoes_lista', name='licitacoes_lista'),
                       )