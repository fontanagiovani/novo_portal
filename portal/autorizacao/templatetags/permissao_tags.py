# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def tem_permissao(user, conteudo):
    return set(conteudo.sites.all()).issubset(user.permissao.sites.all())
