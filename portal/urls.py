# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
# from filebrowser.sites import site


admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'portal.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # (r'^admin/filebrowser/', include(site.urls)),
                       # (r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^summernote/', include('django_summernote.urls')),
                       url(r'^files-widget/', include('topnotchdev.files_widget.urls')),
                       url(r'^$', 'portal.core.views.home', name='home'),
                       url(r'^exemplo_form_admin/', 'portal.core.views.exemplo_form_admin', name='exemplo_form_admin'),
                       )

# Trecho utilizado para que o django sirva os arquivos do summernote
from django.conf import settings

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))