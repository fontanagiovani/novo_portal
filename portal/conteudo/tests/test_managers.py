# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from portal.conteudo.models import Conteudo
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.conteudo.models import Pagina
from portal.conteudo.models import Galeria
from portal.conteudo.models import Video
from portal.conteudo.models import Licitacao


class ConteudoManagerTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Conteudo', _quantity=2, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Conteudo', _quantity=3, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Conteudo', _quantity=4, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Conteudo', _quantity=1, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Conteudo.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class NoticiaManagerTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Noticia', _quantity=2, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Noticia', _quantity=3, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Noticia', _quantity=4, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Noticia', _quantity=1, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Noticia.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class PaginaManagerTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Pagina', _quantity=2, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Pagina', _quantity=3, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Pagina', _quantity=4, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Pagina', _quantity=1, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Pagina.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class EventoManagerTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Evento', _quantity=2, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Evento', _quantity=3, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Evento', _quantity=4, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Evento', _quantity=1, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Evento.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class VideoManagerTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Video', _quantity=2, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Video', _quantity=3, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Video', _quantity=4, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Video', _quantity=1, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Video.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class GaleriaManagerTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Galeria', _quantity=2, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Galeria', _quantity=3, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Galeria', _quantity=4, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Galeria', _quantity=1, titulo=u'Título', campus_origem=campus_origem,
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Galeria.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class LicitacaoManagerTest(TestCase):
    def setUp(self):
        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Licitacao', _quantity=2, titulo=u'Título',
                   data_publicacao=data_passada, publicado=False)

        mommy.make('Licitacao', _quantity=3, titulo=u'Título',
                   data_publicacao=data_passada, publicado=True)

        mommy.make('Licitacao', _quantity=4, titulo=u'Título',
                   data_publicacao=data_futura, publicado=False)

        mommy.make('Licitacao', _quantity=1, titulo=u'Título',
                   data_publicacao=data_futura, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Licitacao.publicados.all().count()
        self.assertEqual(qtd_registros, 3)
