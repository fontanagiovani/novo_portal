# coding: utf-8
from django.contrib.sites.models import Site
from django.http.response import Http404
from portal.core.models import Menu


def carregar_site_e_menus(request):
    try:
        site = Site.objects.get(domain=request.get_host())
        menus = Menu.objects.filter(site__id__exact=site.id)
    except Site.DoesNotExist, Menu.DoesNotExist:
        raise Http404

    return {
        'menus': menus,
        'site': site,
    }