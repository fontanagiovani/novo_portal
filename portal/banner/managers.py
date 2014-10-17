# coding: utf-8
from django.db import models
from django.utils import timezone


class PublicadoManager(models.Manager):
    def get_queryset(self):
        return super(PublicadoManager, self).get_queryset().filter(publicado=True,
                                                                   data_publicacao__lte=timezone.now())


class DestaqueManager(models.Manager):
    def get_queryset(self):
        return super(DestaqueManager, self).get_queryset().filter(publicado=True, tipo=1,
                                                                  data_publicacao__lte=timezone.now())


class LinkDeAcessoManager(models.Manager):
    def get_queryset(self):
        return super(LinkDeAcessoManager, self).get_queryset().filter(publicado=True, tipo=2,
                                                                      data_publicacao__lte=timezone.now())


class GovernamentalManager(models.Manager):
    def get_queryset(self):
        return super(GovernamentalManager, self).get_queryset().filter(publicado=True, tipo=3,
                                                                       data_publicacao__lte=timezone.now())
