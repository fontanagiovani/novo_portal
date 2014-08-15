# coding: utf-8
from portal.core.models import Menu


def carregar_menus(request):
    menus = Menu.objects.all()

    return {
        'menus': menus,
    }