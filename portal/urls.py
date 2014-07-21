# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^summernote/', include('django_summernote.urls')),
                       url(r'^conteudo/', include('portal.conteudo.urls', namespace='conteudo')),
                       url(r'^selecao/', 'portal.core.views.selecao', name='selecao'),
                       url(r'^$', 'portal.core.views.home', name='home'),
                       url(r'^guiadecursos/', 'portal.cursos.views.listagrupodecursos', name='listagrupodecursos'),
                       url(r'^cursos/(?P<campus_id>\d+)/(?P<grupo_id>\d+)/$', 'portal.cursos.views.listacursosdogrupo', name='listacursosdogrupo'),
                       url(r'^curso/(?P<curso_id>\d+)/$', 'portal.cursos.views.exibecurso', name='exibecurso'),
                       )

# Trecho utilizado para que o django sirva os arquivos do summernote
from django.conf import settings

# if settings.DEBUG:
    # static files (images, css, javascript, etc.)
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT}))
