# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import TextInput
from django.db.models import CharField
from embed_video.admin import AdminVideoMixin
import reversion

from portal.core.models import Campus
from portal.core.admin import SitesListFilter, EstaPublicadoListFilter
from portal.conteudo.models import Noticia, Pagina, Evento, Video, Galeria, ImagemGaleria, Anexo, Licitacao, \
    AnexoLicitacao
from portal.conteudo.forms import ConteudoForm, LicitacaoForm, AnexoFormset, NoticiaForm, ImagemGaleriaFormset


class AnexoInLine(admin.TabularInline):
    model = Anexo
    formset = AnexoFormset

    extra = 1

    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': '85'})},
    }


class ConteudoAdmin(reversion.VersionAdmin, admin.ModelAdmin):

    inlines = (AnexoInLine,)
    filter_horizontal = ('galerias', 'videos')

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(ConteudoAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)

        return ModelFormMetaClass

    def get_queryset(self, request):
        qs = super(ConteudoAdmin, self).get_queryset(request)
        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "campus_origem":
            kwargs["queryset"] = Campus.objects.filter(sitedetalhe__site=request.user.permissao.sites.all()).distinct()
        return super(ConteudoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            # somente os sites que o usuario tem permissao ordenados pelo tamanho da string de dominio
            kwargs["queryset"] = request.user.permissao.sites.all().extra(
                select={'length': 'Length(domain)'}).order_by('length')
        return super(ConteudoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class NoticiaAdmin(ConteudoAdmin):
    list_display = ('titulo', 'data_publicacao', 'destaque', 'prioridade_destaque', 'get_publicacao')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = (SitesListFilter, EstaPublicadoListFilter, 'destaque', 'prioridade_destaque')
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'destaque',
                'prioridade_destaque',
                'texto',
                'tags',
            )
        }),
        (u'Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    form = NoticiaForm

admin.site.register(Noticia, NoticiaAdmin)


class PaginaAdmin(ConteudoAdmin):
    list_display = ('titulo', 'data_publicacao', 'get_link', 'get_publicacao', 'pagina_inicial')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = (SitesListFilter, EstaPublicadoListFilter, )
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'texto',
                'tags',
            )
        }),
        (u'Pagina inicial', {
            'classes': ('collapse',),
            'fields': ('pagina_inicial', )
        }),
        (u'Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    form = ConteudoForm

    inlines = (AnexoInLine, )
    filter_horizontal = ('galerias', 'videos')

    def get_link(self, obj):
        return obj.get_absolute_url()
    get_link.short_description = u'Link da página'

admin.site.register(Pagina, PaginaAdmin)


class EventoAdmin(ConteudoAdmin):
    list_display = ('titulo', 'data_publicacao', 'data_inicio', 'data_fim', 'get_publicacao')
    search_fields = ('titulo', 'texto', 'data_publicacao', 'data_inicio', 'data_fim')
    date_hierarchy = 'data_publicacao'
    list_filter = (SitesListFilter, EstaPublicadoListFilter, )
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'local',
                ('data_inicio', 'data_fim'),
                'texto',
                'tags',
            )
        }),
        (u'Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    inlines = (AnexoInLine, )
    filter_horizontal = ('galerias', 'videos')

    form = ConteudoForm

admin.site.register(Evento, EventoAdmin)


class VideoAdmin(AdminVideoMixin, ConteudoAdmin):
    list_display = ('titulo', 'data_publicacao', 'get_publicacao')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = (SitesListFilter, EstaPublicadoListFilter, )
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'url',
                'texto',
                'tags',
            )
        }),
        (u'Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    inlines = (AnexoInLine, )
    filter_horizontal = ('galerias', 'videos')

    form = ConteudoForm

admin.site.register(Video, VideoAdmin)


class ImagemGaleriaInline(admin.TabularInline):
    model = ImagemGaleria

    formset = ImagemGaleriaFormset


class GaleriaAdmin(ConteudoAdmin):
    list_display = ('titulo', 'data_publicacao', 'get_publicacao')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = (SitesListFilter, EstaPublicadoListFilter, )
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'texto',
                'tags',
            )
        }),
        (u'Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    inlines = (ImagemGaleriaInline, )
    filter_horizontal = ('galerias', 'videos')

    form = ConteudoForm

admin.site.register(Galeria, GaleriaAdmin)


class AnexoLicitacaoInLine(admin.TabularInline):

    model = AnexoLicitacao
    extra = 1

    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': '85'})},
    }


class LicitacaoAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    list_display = ('titulo', 'modalidade', 'data_publicacao', 'get_publicacao')
    search_fields = ('modalidade', 'titulo', 'data_publicacao')
    list_filter = (SitesListFilter, EstaPublicadoListFilter, 'modalidade', )
    date_hierarchy = 'data_publicacao'

    inlines = [AnexoLicitacaoInLine, ]
    form = LicitacaoForm

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'modalidade',
                'titulo',
                'data_abertura',
                'pregao_srp',
                'validade_ata_srp',
                'possui_contrato',
                ('vigencia_contrato_inicio', 'vigencia_contrato_fim'),
                'encerrado',
                'situacao',
                'objeto',
                'alteracoes',
                'email_contato',
                'tags',
            )
        }),
        (u'Regras de publicação', {
            'fields': (
                'data_publicacao',
                'publicado',
            )
        }),
    )

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(LicitacaoAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def get_queryset(self, request):
        qs = super(LicitacaoAdmin, self).get_queryset(request)

        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "campus_origem":
            kwargs["queryset"] = Campus.objects.filter(sitedetalhe__site=request.user.permissao.sites.all()).distinct()
        return super(LicitacaoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(LicitacaoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Licitacao, LicitacaoAdmin)
