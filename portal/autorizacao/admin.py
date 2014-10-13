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
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'permissao')
    inlines = [SiteInline]

admin.site.unregister(User)
admin.site.register(User, PermissaoAdmin)