# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from portal.cursos.models import Curso
from portal.core.forms import TinyMCEEditor


class CursoForm(ModelForm):
    class Meta:
        model = Curso
        widgets = {
            'descricao': TinyMCEEditor(),
        }