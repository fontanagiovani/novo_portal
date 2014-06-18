# -*- coding: utf-8 -*-
from django.forms import ModelForm


class NoticiaForm(ModelForm):
    class Media:
        js = ('/static/js/campo_prioridade.js',)