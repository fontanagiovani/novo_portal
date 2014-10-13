# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet

from portal.core.models import Campus
from portal.conteudo.models import Conteudo
from portal.conteudo.models import Licitacao
from portal.core.forms import TinyMCEEditor


class ConteudoForm(ModelForm):
    model = Conteudo

    texto = forms.CharField(widget=TinyMCEEditor())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ConteudoForm, self).__init__(*args, **kwargs)

        if self.request.user.permissao.sites.all().count() == 1:
            self.initial['sites'] = self.request.user.permissao.sites.all()

        if Campus.objects.filter(sitedetalhe__site=self.request.user.permissao.sites.all()).distinct().count() == 1:
            self.initial['campus_origem'] = self.request.user.permissao.sites.first().sitedetalhe.campus

    def clean_sites(self):
        sites_marcados = self.cleaned_data['sites']

        for site in sites_marcados:
            if not site in self.request.user.permissao.sites.all():
                raise forms.ValidationError(u"Você não tem permissão para publicar neste site. "
                                            u"Os sites permitidos são: %s"
                                            % (self.request.user.permissao.sites.all()))

        return sites_marcados


class NoticiaForm(ConteudoForm):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            '/static/js/campo_prioridade.js',
        )


class LicitacaoForm(ModelForm):
    model = Licitacao

    situacao = forms.CharField(widget=TinyMCEEditor())
    objeto = forms.CharField(widget=TinyMCEEditor())
    alteracoes = forms.CharField(widget=TinyMCEEditor())

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            '/static/js/licitacao.js',
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LicitacaoForm, self).__init__(*args, **kwargs)

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


