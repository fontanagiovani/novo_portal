# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from portal.conteudo.models import Noticia
from portal.conteudo.models import Pagina
from portal.conteudo.models import Evento
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria


class NoticiaDetalheTest(TestCase):
    def setUp(self):
        self.noticia = mommy.make(Noticia,
                                  titulo='titulo_teste',
                                  texto=u'texto_teste',
                                  data_publicacao='2014-06-05 10:16:00')
        self.resp = self.client.get(reverse('conteudo:noticia_detalhe', kwargs={'noticia_id': self.noticia.id}))

    def test_get(self):
        """
        GET /conteudo/noticia/1/ deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Noticia detalhe deve renderizar o template noticia.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/noticia.html')

    def test_html(self):
        """
        HTML deve conter o titulo, data, texto
        """
        self.assertContains(self.resp, 'titulo_teste')
        self.assertContains(self.resp, u'texto_teste')
        self.assertContains(self.resp, u'5 de Junho de 2014 às 10:16')


class NoticiaListaTest(TestCase):
    def setUp(self):
        self.noticias = mommy.make(Noticia,
                                   titulo='titulo_teste',
                                   _quantity=50)
        self.resp = self.client.get(reverse('conteudo:noticias_lista'))

    def test_get(self):
        """
        GET /conteudo/noticias/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Noticias lista deve renderizar o template lista.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/noticias_lista.html')

    def test_html(self):
        """
        HTML deve conter o 20 titulos, que e a quantidade para paginacao
        """
        self.assertContains(self.resp, 'titulo_teste', 20)


class PaginaDetalheTest(TestCase):
    def setUp(self):
        self.pagina = mommy.make(Pagina,
                                 titulo='titulo_teste',
                                 texto=u'texto_teste',
                                 data_publicacao='2014-06-05 10:16:00')
        self.resp = self.client.get(reverse('conteudo:pagina_detalhe', kwargs={'pagina_id': self.pagina.id}))

    def test_get(self):
        """
        GET /conteudo/pagina/1/ deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Pagina detalhe deve renderizar o template pagina.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/pagina.html')

    def test_html(self):
        """
        HTML deve conter o titulo, data, texto
        """
        self.assertContains(self.resp, 'titulo_teste')
        self.assertContains(self.resp, u'texto_teste')
        self.assertContains(self.resp, u'5 de Junho de 2014 às 10:16')


class EventoDetalheTest(TestCase):
    def setUp(self):
        self.evento = mommy.make(Evento,
                                 titulo='titulo_teste',
                                 texto=u'texto_teste',
                                 data_publicacao='2014-06-05 10:16:00')
        self.resp = self.client.get(reverse('conteudo:evento_detalhe', kwargs={'evento_id': self.evento.id}))

    def test_get(self):
        """
        GET /conteudo/evento/1/ deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Evento detalhe deve renderizar o template evento.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/evento.html')

    def test_html(self):
        """
        HTML deve conter o titulo, data, texto
        """
        self.assertContains(self.resp, 'titulo_teste')
        self.assertContains(self.resp, u'texto_teste')
        self.assertContains(self.resp, u'5 de Junho de 2014 às 10:16')


class EventoListaTest(TestCase):
    def setUp(self):
        self.eventos = mommy.make(Evento,
                                  titulo='titulo_teste',
                                  _quantity=50)
        self.resp = self.client.get(reverse('conteudo:eventos_lista'))

    def test_get(self):
        """
        GET /conteudo/eventos/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Eventos lista deve renderizar o template lista.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/eventos_lista.html')

    def test_html(self):
        """
        HTML deve conter o 20 titulos, que e a quantidade para paginacao
        """
        self.assertContains(self.resp, 'titulo_teste', 20)

class VideoDetalheTest(TestCase):
    def setUp(self):
        self.video = mommy.make(Video,
                                 titulo='titulo_teste',
                                 texto=u'texto_teste',
                                 video=u'ID_teste',
                                 data_publicacao='2014-06-05 10:16:00')
        self.resp = self.client.get(reverse('conteudo:video_detalhe', kwargs={'video_id': self.video.id}))

    def test_get(self):
        """
        GET /conteudo/video/1/ deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Evento detalhe deve renderizar o template evento.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/video.html')

    def test_html(self):
        """
        HTML deve conter o titulo, data, texto
        """
        self.assertContains(self.resp, 'titulo_teste')
        self.assertContains(self.resp, u'texto_teste')
        self.assertContains(self.resp, u'ID_teste')
        self.assertContains(self.resp, u'5 de Junho de 2014 às 10:16')


class VideosListaTest(TestCase):
    def setUp(self):
        self.videos = mommy.make(Video,
                                  titulo='titulo_teste',
                                  _quantity=50)
        self.resp = self.client.get(reverse('conteudo:videos_lista'))

    def test_get(self):
        """
        GET /conteudo/videos/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Videos lista deve renderizar o template lista.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/videos_lista.html')

    def test_html(self):
        """
        HTML deve conter o 40 titulos,(20 para titulo da noticia, 20 para o alt da imagem) que e a quantidade para paginacao
        """
        self.assertContains(self.resp, 'titulo_teste', 40)

class GaleriaDetalheTest(TestCase):
    def setUp(self):
        self.galeria = mommy.make(Galeria,
                                 titulo='titulo_teste',
                                 texto=u'texto_teste',
                                 data_publicacao='2014-06-05 10:16:00')
        self.resp = self.client.get(reverse('conteudo:galeria_detalhe', kwargs={'galeria_id': self.galeria.id}))

    def test_get(self):
        """
        GET /conteudo/galeria/1/ deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Evento detalhe deve renderizar  o template evento.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/galeria.html')

    def test_html(self):
        """
        HTML deve conter o titulo, data, texto
        """
        self.assertContains(self.resp, 'titulo_teste')
        self.assertContains(self.resp, u'texto_teste')
        self.assertContains(self.resp, u'5 de Junho de 2014 às 10:16')


class GaleriaListaTest(TestCase):
    def setUp(self):
        self.eventos = mommy.make(Galeria,
                                  titulo='titulo_teste',
                                  _quantity=50)
        self.resp = self.client.get(reverse('conteudo:galerias_lista'))

    def test_get(self):
        """
        GET /conteudo/galerias/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Eventos lista deve renderizar o template lista.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/galerias_lista.html')

    def test_html(self):
        """
        HTML deve conter o 20 titulos, que e a quantidade para paginacao
        """
        self.assertContains(self.resp, 'titulo_teste', 20)