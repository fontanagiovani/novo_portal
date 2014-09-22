#coding: utf-8
from django import forms
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido


def _generic_clean_sites(obj):
    sites_marcados = obj.cleaned_data['sites']
    for site in sites_marcados:
        if not site in obj.request.user.permissao.sites.all():
            raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                        u"Os sites permitidos são: %s"
                                        % (obj.request.user.permissao.sites.all()))

    return sites_marcados


class BannerForm(forms.ModelForm):
    model = Banner

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BannerForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        return _generic_clean_sites(self)


class BannerAcessoRapidoForm(forms.ModelForm):
    model = BannerAcessoRapido

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BannerAcessoRapidoForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        return _generic_clean_sites(self)