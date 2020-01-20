# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from conteudo.models import Noticia
from django.conf import settings



class CorrectMimeTypeFeed(Atom1Feed):
    mime_type = 'application/xml'

class UltimasNoticias(Feed):
    title = u'Notícias do IFMT'
    description = u'Notícias mais recentes do IFMT'
    link = '/rss/'
    language = settings.LANGUAGE_CODE
    feed_type = CorrectMimeTypeFeed

    def items(self):
        return Noticia.publicados.filter(sites__id__exact=1)[:5]

    # def item_link(self, item):
    #     return '/conteudo/noticia/'
    # vai usar get_absolute_url(self):

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return item.titulo

    def item_pubdate(self, item):
        return item.data_publicacao
