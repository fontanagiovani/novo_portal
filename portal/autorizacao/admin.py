# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
import reversion

from portal.autorizacao.models import Permissao
from portal.autorizacao.forms import PermissaoFormset


class LogAtividadesListFilter(admin.SimpleListFilter):
    # USAGE
    # list_filter = (CategoryListFilter,)

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Usou o sistema?'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'usou'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = list()
        list_tuple.append((1, u'Sim'))
        list_tuple.append((0, u'Não'))
        # for site in request.user.permissao.sites.all():
        #     list_tuple.append((site.id, site.domain))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            if self.value() == '0':
                usuarios_sem_atividade = list(queryset.values_list('id', flat=True).annotate(
                    logs=Count('logentry__id')).filter(logs=0))
                return queryset.filter(id__in=usuarios_sem_atividade)
            else:
                usuarios_sem_atividade = list(queryset.values_list('id', flat=True).annotate(
                    logs=Count('logentry__id')).filter(logs__gt=0))
                return queryset.filter(id__in=usuarios_sem_atividade)
        else:
            return queryset


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
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', LogAtividadesListFilter)

    def log_atividade(self, obj):
        if obj.logentry_set.all().exists():
            return True
        else:
            return False

    log_atividade.short_description = u'Usou o sistema?'
    log_atividade.boolean = True

admin.site.unregister(User)
admin.site.register(User, PermissaoAdmin)