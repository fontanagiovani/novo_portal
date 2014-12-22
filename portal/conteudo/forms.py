# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet

from portal.core.models import Campus
from portal.conteudo.models import Conteudo
from portal.conteudo.models import Licitacao
from portal.core.forms import TinyMCEEditor


class ConteudoForm(ModelForm):
    class Meta:
        model = Conteudo

        fields = ('campus_origem', 'titulo', 'slug', 'texto', 'data_publicacao', 'galerias', 'videos', 'tags',
                  'sites', 'publicado')

        widgets = {
            'texto': TinyMCEEditor(),
        }

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
    class Meta:
        model = Licitacao

        fields = ('sites', 'campus_origem', 'modalidade', 'titulo', 'data_publicacao', 'data_abertura', 'pregao_srp',
                  'validade_ata_srp', 'possui_contrato', 'vigencia_contrato_inicio', 'vigencia_contrato_fim',
                  'encerrado', 'situacao', 'objeto', 'alteracoes', 'email_contato', 'publicado', 'tags')

        widgets = {
            'situacao': TinyMCEEditor(),
        }

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
            tamanho_adequado = False
            primeira_imagem = True

            for cleaned_data in self.cleaned_data:
                if not cleaned_data.get('DELETE', False):
                    try:
                        imagem = cleaned_data.get('arquivo').image

                        # restringe que a primeira imagem obedeca a resolucao minima (980x388) quando destaque
                        if imagem and primeira_imagem:
                            primeira_imagem = False
                            if imagem.width >= 980 and imagem.height >= 388:
                                tamanho_adequado = True
                    except:
                        pass

            if not imagem:
                raise forms.ValidationError(u'Uma notícia de destaque precisa de uma imagem anexada.')
            if imagem and not tamanho_adequado:
                raise forms.ValidationError(u'Uma notícia de destaque precisa que a primeira imagem anexada '
                                            u'tenha resolução de no mínimo 980x388 (largura x altura). A atual '
                                            u'primeira imagem possui %dx%d.' % (imagem.width, imagem.height))


class ImagemGaleriaFormset(BaseInlineFormSet):
    def clean(self):
        super(ImagemGaleriaFormset, self).clean()

        # se houver erros no formset ja retorna para tratamento
        if any(self.errors):
            return

        imagem = False

        for cleaned_data in self.cleaned_data:
            if not cleaned_data.get('DELETE', False):
                try:
                    imagem = cleaned_data.get('imagem').image
                except:
                    pass

        if not imagem:
            raise forms.ValidationError(u'Uma galeria precisa de uma imagem anexada.')
