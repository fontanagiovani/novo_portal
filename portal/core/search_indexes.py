# coding: utf-8
from haystack import indexes
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.conteudo.models import Pagina
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria


class NoticiaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    texto = indexes.CharField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')

    def get_model(self):
        return Noticia

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class EventoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    texto = indexes.CharField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')

    def get_model(self):
        return Evento

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PaginaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    texto = indexes.CharField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')

    def get_model(self):
        return Pagina

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    texto = indexes.CharField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')

    def get_model(self):
        return Video

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class GaleriaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    texto = indexes.CharField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')

    def get_model(self):
        return Galeria

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
