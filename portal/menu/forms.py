# -*- coding: utf-8 -*-
from django import forms
from portal.menu.models import Menu


class MenuForm(forms.ModelForm):
    model = Menu

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MenuForm, self).__init__(*args, **kwargs)

    def clean_site(self):
        site_marcado = self.cleaned_data['site']

        if not site_marcado in self.request.user.permissao.sites.all():
            raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                        u"Os sites permitidos são: %s"
                                        % (self.request.user.permissao.sites.all()))

        return site_marcado
