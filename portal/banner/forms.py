# coding: utf-8
from django import forms
from portal.banner.models import Banner


class BannerForm(forms.ModelForm):
    model = Banner

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BannerForm, self).__init__(*args, **kwargs)
        # self.fields['sites'].help_text = u'Mantenha a tecla "Control", ou "Command" no Mac, pressionado para ' \
        #                                  u'selecionar mais de uma opção.'
        if self.request.user.permissao.sites.all().count() == 1:
            self.initial['sites'] = self.request.user.permissao.sites.all()

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']
        for site in sites_marcados:
            if site not in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados

    def clean_arquivo(self):
        imagem = False
        tamanho_adequado = False

        try:
            imagem = self.cleaned_data['arquivo'].image

            if imagem.width >= 900 and imagem.height >= 240:
                tamanho_adequado = True

        except:
            pass

        if imagem and not tamanho_adequado:
            raise forms.ValidationError(u'Um banner precisa ter uma imagem com resolução de no mínimo 900x240 '
                                        u'(largura x altura). '
                                        u'A atual imagem possui %dx%d.' % (imagem.width, imagem.height))

        return imagem
