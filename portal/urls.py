# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'portal.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'portal.core.views.home', name='home'),
                       url(r'^site/', 'portal.core.views.site', name='site'),
                       )
