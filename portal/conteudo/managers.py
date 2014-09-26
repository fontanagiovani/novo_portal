#coding: utf-8
from django.db import models
from django.utils import timezone


class ConteudoPublicadoManager(models.Manager):
    def get_queryset(self):
        return super(ConteudoPublicadoManager, self).get_queryset().filter(publicado=True,
                                                                           data_publicacao__lte=timezone.now())