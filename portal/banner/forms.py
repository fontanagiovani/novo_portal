#coding: utf-8
from django import forms
from portal.banner.models import Banner


class BannerForm(forms.ModelForm):
    model = Banner

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BannerForm, self).__init__(*args, **kwargs)
        if self.request.user.permissao.sites.all().count() == 1:
            self.initial['sites'] = self.request.user.permissao.sites.all()

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']
        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados
