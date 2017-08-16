# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Agenda(models.Model):
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição do compromisso', help_text=u'No máximo 250 caracteres')
    inicio = models.DateTimeField(verbose_name=u'data e hora de início do compromisso')
    fim = models.DateTimeField(verbose_name=u'data e hora do fim do compromisso')
    local = models.CharField(max_length=100, verbose_name=u'Local do compromisso', help_text=u'No máximo 100 caracteres', blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_ultima_modificacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'Compromisso'
        verbose_name_plural = u'Compromissos'

    def __unicode__(self):
        return self.descricao
