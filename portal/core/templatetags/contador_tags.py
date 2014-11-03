# -*- coding: utf-8 -*-
from django import template
from portal.core.models import ContadorVisitas


register = template.Library()


@register.simple_tag(takes_context=True)
def contador(context):
    """
    Displays pageviews of the current page.
    """
    try:
        request = context['request']
        cont = ContadorVisitas.objects.get(url=request.path)
        return cont.contagem
    except ContadorVisitas.DoesNotExist:
        return 0


@register.simple_tag
def contador_url(path):
    """
    Displays pageviews by url. Useful for list views.
    """
    try:
        cont = ContadorVisitas.objects.get(url=path)
        return cont.contagem
    except ContadorVisitas.DoesNotExist:
        return 0