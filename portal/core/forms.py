# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from portal.core.models import Curso
from portal.core.models import Site
from portal.core.models import Menu
from portal.core.models import MenuContainer


class CursoForm(ModelForm):
    class Meta:
        model = Curso


class SiteForm(ModelForm):
    class Meta:
        model = Site

    nome = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))


class MenuForm(ModelForm):
    class Meta:
        model = Menu


class MenuContainerForm(ModelForm):
    class Meta:
        model = MenuContainer