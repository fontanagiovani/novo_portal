#coding: utf-8
from django.db import models
from django.utils import timezone


class PublicadoManager(models.Manager):
    def get_queryset(self):
        return super(PublicadoManager, self).get_queryset().filter(publicado=True,
                                                                           data_publicacao__lte=timezone.now())