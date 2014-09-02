# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import BaseInlineFormSet
from portal.core.models import Menu
from portal.core.models import SiteDetalhe


class MenuForm(forms.ModelForm):
    model = Menu

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MenuForm, self).__init__(*args, **kwargs)

    def clean_site(self):
        site_marcado = self.cleaned_data['site']

        if not site_marcado in self.request.user.permissaopublicacao.sites.all():
            raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                        u"Os sites permitidos são: %s"
                                        % (self.request.user.permissaopublicacao.sites.all()))

        return site_marcado


class SiteDetalheForm(forms.ModelForm):
    model = SiteDetalhe

    endereco = forms.CharField(widget=forms.Textarea)


class SiteDetalheFormset(BaseInlineFormSet):
    # pass
    def clean(self):
        """Check that at least one service has been entered."""
        super(SiteDetalheFormset, self).clean()

        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('Você deve preencher os dois campos abaixo.')
