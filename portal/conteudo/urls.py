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

                       url(r'^video/(?P<video_id>\d+)/$', 'video_detalhe', name='video_detalhe'),
                       url(r'^videos/$', 'videos_lista', name='videos_lista'),
                       )