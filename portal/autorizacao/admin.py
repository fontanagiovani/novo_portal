from django.contrib import admin
from portal.autorizacao.models import Permissao
from django.contrib.auth.admin import User
from django.contrib.auth.admin import UserAdmin


class SiteInline(admin.StackedInline):
    model = Permissao
    max_num = 1
    can_delete = False


class PermissaoAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'permissao')
    inlines = [SiteInline]

admin.site.unregister(User)
admin.site.register(User, PermissaoAdmin)