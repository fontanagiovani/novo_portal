#coding: utf-8
from django.db import models


class ConteudoPublicadoManager(models.Manager):
    def get_queryset(self):
        return super(ConteudoPublicadoManager, self).get_queryset().filter(publicar=True)