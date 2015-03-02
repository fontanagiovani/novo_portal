# -*- coding: utf-8 -*-
from django.shortcuts import redirect


class RemoveWWWRedirectMiddleware(object):
    """
    Esse middleware remove o www. inicial nas urls que sao requisitadas
    """
    def process_request(self, request):
        url = request.build_absolute_uri()
        if url.startswith('www.'):
            url = url.replace('www.', '')

            return redirect(url)