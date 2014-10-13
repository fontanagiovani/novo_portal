# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import BaseInlineFormSet


class PermissaoFormset(BaseInlineFormSet):
    def clean(self):
        super(PermissaoFormset, self).clean()

        # se houver erros no formset ja retorna para tratamento
        if any(self.errors):
            return

        for cleaned_data in self.cleaned_data:
            if not cleaned_data.get('sites', False):
                raise forms.ValidationError(u'Um usuário deve administrar pelo menos um site')
