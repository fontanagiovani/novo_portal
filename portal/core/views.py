# coding: utf-8
from django.shortcuts import render


def home(request):
    return render(request, 'core/base.html')


def site(request):
    return render(request, 'core/site.html')
