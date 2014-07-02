# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^summernote/', include('django_summernote.urls')),
                       url(r'^conteudo/', include('portal.conteudo.urls', namespace='conteudo')),
                       url(r'^$', 'portal.core.views.home', name='home'),
                       url(r'^conteudo/(?P<conteudo_id>\d+)/', 'portal.core.views.conteudo_detalhe',
                           name='conteudo_detalhe'),
                       url(r'^thumbnail/(?P<conteudo_id>\d+)/', 'portal.core.views.thumbnail', name='thumbnail'),
                       )

# Trecho utilizado para que o django sirva os arquivos do summernote
from django.conf import settings

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))