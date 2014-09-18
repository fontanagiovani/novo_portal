# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User


class Permissao(models.Model):
    class Meta:
        verbose_name = u'Permissão de Publicacão'
        verbose_name_plural = u'Permissões de Publicação'

    sites = models.ManyToManyField(Site, verbose_name=u'Sites Permitidos')
    user = models.OneToOneField(User, verbose_name=u'Usuario')

    def __unicode__(self):
        return self.sites.all()