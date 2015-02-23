# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Permissao(models.Model):
    class Meta:
        verbose_name = _(u'Permissao de Publicacao')
        verbose_name_plural = _(u'Permissoes de Publicacao')

    sites = models.ManyToManyField(Site, verbose_name=u'Sites Permitidos')
    user = models.OneToOneField(User, verbose_name=u'Usuário')

    def __unicode__(self):
        return str(self.sites.all())