from django.shortcuts import render
import os
from django.conf import settings

# Create your views here.

def download(request):
    if request.method == 'POST':
        return render(request, 'dirf/busca.html', {})
    else:
        patch = os.path.join(settings.MEDIA_ROOT, 'dirf')
        diretorios = [ name for name in os.listdir(patch) if os.path.isdir(os.path.join(patch, name)) ]
        return render(request, 'dirf/busca.html', {'diretorios': diretorios})