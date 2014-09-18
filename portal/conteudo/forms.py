# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet

from portal.conteudo.models import Pagina
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento


class NoticiaForm(ModelForm):
    model = Noticia

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            '/static/js/campo_prioridade.js',
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(NoticiaForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class PaginaForm(ModelForm):
    model = Pagina

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PaginaForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class EventoForm(ModelForm):
    model = Evento

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EventoForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class VideoForm(ModelForm):
    model = Evento

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VideoForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class GaleriaForm(ModelForm):
    model = Evento

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GaleriaForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class LicitacaoForm(ModelForm):
    model = Evento

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            '/static/js/licitacao.js',
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LicitacaoForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class AnexoFormset(BaseInlineFormSet):
    def clean(self):
        super(AnexoFormset, self).clean()

        # se houver erros no formset ja retorna para tratamento
        if any(self.errors):
            return

        # se o campo destaque estiver selecionado faz a validacao
        if self.data.get('destaque'):
            imagem = False

            for cleaned_data in self.cleaned_data:
                if not cleaned_data.get('DELETE', False):
                    try:
                        imagem = cleaned_data.get('arquivo').image
                    except:
                        pass

            if not imagem:
                raise forms.ValidationError(u'Uma notícia de destaque precisa de uma imagem anexada.')