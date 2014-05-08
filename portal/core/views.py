# coding: utf-8
from portal.core.forms import SiteForm
from portal.core.forms import MenuContainerForm
from django.shortcuts import render


def home(request):
    return render(request, 'core/base.html')


def exemplo_form_admin(request):
    return render(request, 'core/exemplo_form_admin.html', {'form': SiteForm()})
