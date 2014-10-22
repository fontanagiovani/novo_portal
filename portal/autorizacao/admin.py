# -*- coding: utf-8 -*-
from django.contrib import admin
from portal.autorizacao.models import Permissao
from django.contrib.auth.admin import User
from django.contrib.auth.admin import UserAdmin
import reversion

from portal.autorizacao.forms import PermissaoFormset


class SiteInline(admin.StackedInline):
    model = Permissao
    formset = PermissaoFormset
    max_num = 1
    can_delete = False

    filter_horizontal = ('sites', )


class PermissaoAdmin(reversion.VersionAdmin, UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'log_atividade', 'date_joined', 'last_login',
                    'is_staff', 'permissao')
    inlines = [SiteInline]
    date_hierarchy = 'last_login'

    def log_atividade(self, obj):
        if obj.logentry_set.all().exists():
            return True
        else:
            return False

    log_atividade.short_description = u'Log de atividade'
    log_atividade.boolean = True

admin.site.unregister(User)
admin.site.register(User, PermissaoAdmin)