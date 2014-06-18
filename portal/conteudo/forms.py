# -*- coding: utf-8 -*-
from django.forms import ModelForm


class NoticiaForm(ModelForm):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            '/static/js/campo_prioridade.js',
        )