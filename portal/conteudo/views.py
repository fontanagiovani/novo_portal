# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from portal.conteudo.models import Noticia


def noticia_detalhe(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)

    return render(request, 'conteudo/noticia.html', {'noticia': noticia})