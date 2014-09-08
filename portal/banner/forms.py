#coding: utf-8
from django import forms
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido


class BannerForm(forms.ModelForm):
    model = Banner

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BannerForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissaopublicacao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permtrelloissaopublicacao.sites.all()))

        return sites_marcados


class BannerAcessoRapidoForm(forms.ModelForm):
    model = BannerAcessoRapido

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BannerAcessoRapidoForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissaopublicacao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissaopublicacao.sites.all()))

        return sites_marcados

