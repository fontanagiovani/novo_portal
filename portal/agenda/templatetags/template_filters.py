# -*- coding: utf-8 -*-
from django.template.base import Library
# from datetime import datetime # usado para a função plus_days para somar datas
import datetime # usado para a função plus_days para somar datas

register = Library()

# retorna item de dicionário
#@register.filter
#def get_item(dictionary, key):
#    return dictionary.get(key)

# retorna a variável no tipo inteiro
@register.filter
def to_int(value):
    return int(value)

# retorna o tipo de variável utilizada
@register.filter
def get_type(value):
    return type(value)

# adiciona dias em uma data
@register.filter
def plus_days(value, days):
    return value + datetime.timedelta(days=days)

# subtrai dias em uma data
@register.filter
def minus_days(value, days):
    return value - datetime.timedelta(days=days)
