# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.core.models import Conteudo
from portal.core.models import Midia

1

class MidiaInLine(admin.StackedInline):
    model = Midia
    extra = 1


class ConteudoAdmin(SummernoteModelAdmin):
    inlines = (MidiaInLine, )

admin.site.register(Conteudo, ConteudoAdmin)