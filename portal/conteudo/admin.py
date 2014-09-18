# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import TextInput
from django.db.models import CharField
from django_summernote.admin import SummernoteModelAdmin

from portal.conteudo.models import Noticia, Pagina, Evento, Video, Galeria
from portal.conteudo.models import ImagemGaleria
from portal.conteudo.models import Anexo
from portal.conteudo.models import Licitacao
from portal.conteudo.models import AnexoLicitacao

from portal.conteudo.forms import NoticiaForm
from portal.conteudo.forms import EventoForm
from portal.conteudo.forms import PaginaForm
from portal.conteudo.forms import VideoForm
from portal.conteudo.forms import GaleriaForm
from portal.conteudo.forms import LicitacaoForm
from portal.conteudo.forms import AnexoFormset


class AnexoInLine(admin.StackedInline):
    model = Anexo
    formset = AnexoFormset

    extra = 1


class NoticiaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'destaque', 'prioridade_destaque')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('destaque', 'prioridade_destaque')
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
                'fonte',
                'data_publicacao',
                'tags',
            )
        }),
        ('Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
    )

    form = NoticiaForm

    inlines = (AnexoInLine,)
    filter_horizontal = ('galerias', 'videos')

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
    list_display = ('titulo', 'data_publicacao', 'get_link')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'texto',
                'fonte',
                'data_publicacao',
                'tags',
            )
        }),
        ('Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
    )

    inlines = (AnexoInLine, )
    filter_horizontal = ('galerias', 'videos')

    def get_link(self, obj):
        return obj.get_absolute_url()
    get_link.short_description = u'Link da página'

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
    list_display = ('titulo', 'data_publicacao', 'data_inicio', 'data_fim')
    search_fields = ('titulo', 'texto', 'data_publicacao', 'data_inicio', 'data_fim')
    date_hierarchy = 'data_publicacao'
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'local',
                'data_inicio',
                'data_fim',
                'texto',
                'fonte',
                'data_publicacao',
                'tags',
            )
        }),
        ('Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
    )

    inlines = (AnexoInLine, )
    filter_horizontal = ('galerias', 'videos')

    form = EventoForm

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
    list_display = ('titulo', 'data_publicacao')
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('campus_origem', 'data_publicacao')
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
                'fonte',
                'data_publicacao',
                'tags',
            )
        }),
        ('Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
    )

    inlines = (AnexoInLine, )
    filter_horizontal = ('galerias', 'videos')

    form = VideoForm

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
    extra = 5


class GaleriaAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'data_publicacao',)
    search_fields = ('titulo', 'texto', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    list_filter = ('campus_origem', 'data_publicacao')
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'campus_origem',
                'titulo',
                'slug',
                'texto',
                'fonte',
                'data_publicacao',
                'tags',
            )
        }),
        ('Galerias e Vídeos', {
            'classes': ('collapse',),
            'fields': ('galerias', 'videos')
        }),
    )

    inlines = (ImagemGaleriaInline, )
    filter_horizontal = ('galerias', 'videos')

    form = GaleriaForm

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


class AnexoLicitacaoInLine(admin.StackedInline):

    model = AnexoLicitacao
    extra = 1

    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': '115'})},
    }


class LicitacaoAdmin(SummernoteModelAdmin):
    list_display = ('modalidade', 'titulo', 'data_publicacao')
    search_fields = ('modalidade', 'titulo', 'data_publicacao')
    list_filter = ('sites', 'modalidade', 'pregao_srp', 'possui_contrato')
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
