# coding: utf-8
from haystack import indexes

from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.conteudo.models import Pagina
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria
from portal.conteudo.models import Licitacao


class NoticiaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.NgramField(model_attr='titulo')
    texto = indexes.NgramField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')
    sites = indexes.MultiValueField()

    def get_model(self):
        return Noticia

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class EventoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.NgramField(model_attr='titulo')
    texto = indexes.NgramField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')
    sites = indexes.MultiValueField()

    def get_model(self):
        return Evento

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PaginaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.NgramField(model_attr='titulo')
    texto = indexes.NgramField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')
    sites = indexes.MultiValueField()

    def get_model(self):
        return Pagina

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.NgramField(model_attr='titulo')
    texto = indexes.NgramField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')
    sites = indexes.MultiValueField()

    def get_model(self):
        return Video

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class GaleriaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.NgramField(model_attr='titulo')
    texto = indexes.NgramField(model_attr='texto')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')
    sites = indexes.MultiValueField()

    def get_model(self):
        return Galeria

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().publicados.all()


class LicitacaoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    modalidade = indexes.NgramField(model_attr='modalidade')
    titulo = indexes.NgramField(model_attr='titulo')
    situacao = indexes.NgramField(model_attr='situacao')
    objeto = indexes.NgramField(model_attr='objeto')
    alteracoes = indexes.NgramField(model_attr='alteracoes')
    data_publicacao = indexes.CharField(model_attr='data_publicacao')
    data_abertura = indexes.CharField(model_attr='data_abertura')
    sites = indexes.MultiValueField()

    def get_model(self):
        return Licitacao

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().publicados.all()
