# -*- coding: utf-8 -*-
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from portal.conteudo.models import Noticia, Pagina, Evento, Video, Galeria
from portal.conteudo.models import ImagemGaleria
from portal.conteudo.models import Anexo
from portal.conteudo.forms import NoticiaForm
from portal.conteudo.forms import EventoForm
from portal.conteudo.forms import PaginaForm


class AnexoInLine(admin.StackedInline):
    model = Anexo
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
        ModelForm = super(NoticiaAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass

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
        ModelForm = super(PaginaAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass


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
        ModelForm = super(EventoAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass


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

admin.site.register(Galeria, GaleriaAdmin)
