# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import TextInput
from django.db.models import CharField
from django_summernote.admin import SummernoteModelAdmin

from portal.core.admin import SitesListFilter, EstaPublicadoListFilter
from portal.conteudo.models import Noticia, Pagina, Evento, Video, Galeria, ImagemGaleria, Anexo, Licitacao, \
    AnexoLicitacao
from portal.conteudo.forms import NoticiaForm, EventoForm, PaginaForm, VideoForm, GaleriaForm, LicitacaoForm, \
    AnexoFormset


class AnexoInLine(admin.TabularInline):
    model = Anexo
    formset = AnexoFormset

    extra = 1

    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': '85'})},
    }


class NoticiaAdmin(SummernoteModelAdmin):
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
        ('Galerias e Vídeos', {
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

    inlines = (AnexoInLine,)
    filter_horizontal = ('galerias', 'videos')

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(NoticiaAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(NoticiaAdmin, self).queryset(request)
        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(NoticiaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Noticia, NoticiaAdmin)


class PaginaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'get_link', 'get_publicacao')
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
        ('Galerias e Vídeos', {
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

    def get_link(self, obj):
        return obj.get_absolute_url()
    get_link.short_description = u'Link da página'

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    form = PaginaForm

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(PaginaAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(PaginaAdmin, self).queryset(request)

        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(PaginaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Pagina, PaginaAdmin)


class EventoAdmin(SummernoteModelAdmin):
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
        ('Galerias e Vídeos', {
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

    form = EventoForm

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(EventoAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)

        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(EventoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Evento, EventoAdmin)


class VideoAdmin(SummernoteModelAdmin):
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
                'id_video_youtube',
                'texto',
                'tags',
            )
        }),
        ('Galerias e Vídeos', {
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

    form = VideoForm

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(VideoAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(VideoAdmin, self).queryset(request)

        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(VideoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Video, VideoAdmin)


class ImagemGaleriaInline(admin.TabularInline):
    model = ImagemGaleria


class GaleriaAdmin(SummernoteModelAdmin):
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
        ('Galerias e Vídeos', {
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

    form = GaleriaForm

    def get_publicacao(self, obj):
        return obj.esta_publicado
    get_publicacao.short_description = u'Publicado'
    get_publicacao.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(GaleriaAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(GaleriaAdmin, self).queryset(request)

        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(GaleriaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Galeria, GaleriaAdmin)


class AnexoLicitacaoInLine(admin.TabularInline):

    model = AnexoLicitacao
    extra = 1

    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': '85'})},
    }


class LicitacaoAdmin(SummernoteModelAdmin):
    list_display = ('modalidade', 'titulo', 'data_publicacao')
    search_fields = ('modalidade', 'titulo', 'data_publicacao')
    list_filter = (SitesListFilter, 'modalidade', )
    date_hierarchy = 'data_publicacao'

    inlines = [AnexoLicitacaoInLine, ]
    form = LicitacaoForm

    def get_form(self, request, obj=None, **kwargs):
        modelform = super(LicitacaoAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(modelform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return modelform(*args, **kwargs)
        return ModelFormMetaClass

    def queryset(self, request):
        qs = super(LicitacaoAdmin, self).queryset(request)

        excluidos = Site.objects.exclude(id__in=request.user.permissao.sites.values_list('id'))

        return qs.exclude(sites__in=excluidos)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["queryset"] = request.user.permissao.sites.all()
        return super(LicitacaoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Licitacao, LicitacaoAdmin)
