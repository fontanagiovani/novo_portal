# -*- coding: utf-8 -*-

from django.shortcuts import render
import os
from django.conf import settings
from django.http.response import HttpResponse
from django.core.servers.basehttp import FileWrapper

# Create your views here.

# exemplo de download de: https://djangosnippets.org/snippets/365/

# tipos de mensagem: success, warning, info, alert, secondary

def download(request):
    patch = os.path.join(settings.MEDIA_ROOT, 'dirf')
    diretorios = [ name for name in os.listdir(patch) if os.path.isdir(os.path.join(patch, name)) ]

    if request.method == 'POST':
        if (request.POST.get('ano', None) and request.POST.get('cnpj', None)):
            cnpj = request.POST.get('cnpj', None).replace('.', '').replace('-', '').replace('/', '')
            if os.path.isfile(patch + '/' + request.POST.get('ano', None) + '/' + cnpj + '.pdf'):
                filename = patch + '/' + request.POST.get('ano', None) + '/' + cnpj + '.pdf' # Select your file here
                wrapper = FileWrapper(file(filename))
                response = HttpResponse(wrapper, content_type='application/pdf; charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename=%s.pdf' % (cnpj) # para baixar arquivo em vez de exibir no navegador
                response['Content-Length'] = os.path.getsize(filename)
                return response
                # return render(request, 'dirf/busca.html', {'diretorios': diretorios, 'mensagem': u'Dirf encontrada com sucesso!', 'tipo': 'success'})
            else:
                return render(request, 'dirf/busca.html', {'diretorios': diretorios, 'mensagem': u'Arquivo não encontrado para esse CNPJ', 'tipo': 'warning'})
        else:
            return render(request, 'dirf/busca.html', {'diretorios': diretorios, 'mensagem': u'O ano calendário e CNPJ são obrigatórios', 'tipo': 'alert'})
    else:
        return render(request, 'dirf/busca.html', {'diretorios': diretorios,})