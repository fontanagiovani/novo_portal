# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils import timezone

from model_mommy import mommy


class NoticiaDetalheTest(TestCase):
    def setUp(self):
        self.obj = mommy.make('Noticia', titulo='titulo_teste', texto=u'texto_teste',
                              data_publicacao='2014-06-05T10:16:00-04:00',)
        self.site = mommy.make(Site, domain='rtr.ifmt.dev')
        self.obj.sites.add(self.site)
        self.obj.tags.add('ifmt-teste')

        self.resp = self.client.get(reverse('conteudo:noticia_detalhe', kwargs={'slug': self.obj.slug}),
                                    SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET /conteudo/noticia/<slug>/ deve retorno status code 200
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
        self.assertContains(self.resp, 'ifmt-teste')


class NoticiaListaTest(TestCase):
    def setUp(self):
        self.noticias = mommy.make(
            'Noticia',
            titulo='titulo_teste',
            _quantity=50,
            campus_origem=mommy.make('Campus'),
        )
        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]
        for i in self.noticias:
            i.sites.add(self.site)

        # trecho cria um novo site e novas noticias para simular o ambiente real
        self.site2 = mommy.make('Site', domain='cba.ifmt.dev')
        self.noticias = mommy.make(
            'Noticia',
            titulo='titulo_teste',
            _quantity=10,
            campus_origem=mommy.make('Campus', slug='campus2'),
        )
        for i in self.noticias:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('conteudo:noticias_lista'), SERVER_NAME='rtr.ifmt.dev')

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
        self.obj = mommy.make(
            'Pagina',
            titulo='titulo_teste',
            texto=u'texto_teste',
            data_publicacao='2014-06-05T10:16:00-04:00',
            # data_publicacao='2014-06-05 10:16:00'
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        self.obj.sites.add(self.site)
        self.obj.tags.add('ifmt-teste')

        self.resp = self.client.get(reverse('conteudo:pagina_detalhe',
                                            kwargs={'slug': self.obj.slug}), SERVER_NAME='rtr.ifmt.dev')

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
        self.assertContains(self.resp, 'ifmt-teste')


class EventoDetalheTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(
            'Evento',
            titulo='titulo_teste',
            texto=u'texto_teste',
            local=u'Reitoria',
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        self.obj.sites.add(self.site)
        self.obj.tags.add('ifmt-teste')

        self.resp = self.client.get(reverse('conteudo:evento_detalhe',
                                            kwargs={'slug': self.obj.slug}), SERVER_NAME='rtr.ifmt.dev')

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
        self.assertContains(self.resp, u'Reitoria')
        self.assertContains(self.resp, 'ifmt-teste')


class EventoListaTest(TestCase):
    def setUp(self):
        self.eventos = mommy.make(
            'Evento',
            titulo='titulo_teste',
            _quantity=50,
            campus_origem=mommy.make('Campus'),
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        for i in self.eventos:
            i.sites.add(self.site)

        # trecho cria um novo site e novos videos para simular o ambiente real
        self.site2 = mommy.make('Site', domain='cba.ifmt.dev')
        self.eventos = mommy.make(
            'Evento',
            titulo='titulo_teste',
            _quantity=10,
            campus_origem=mommy.make('Campus', slug='campus2'),
        )
        for i in self.eventos:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('conteudo:eventos_lista'), SERVER_NAME='rtr.ifmt.dev')

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
        # data_passada = timezone.now() - timezone.timedelta(days=1)
        self.obj = mommy.make(
            'Video',
            titulo='titulo_teste',
            texto=u'texto_teste',
            id_video_youtube=u'ID_teste',
            data_publicacao='2014-06-05T10:16:00-04:00',
            campus_origem=mommy.make('Campus'),
            publicado=True,
        )

        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        self.obj.tags.add('ifmt-teste')
        # as views de detalhe nao precisam de um site para ser exibida, para permitir o relacionamento entre
        # os conteudos dos sites
        # self.video.sites.add(self.site)

        self.resp = self.client.get(reverse('conteudo:video_detalhe',
                                            kwargs={'slug': self.obj.slug}), SERVER_NAME=self.site.domain)

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
        self.assertContains(self.resp, 'ifmt-teste')


class VideosListaTest(TestCase):
    def setUp(self):
        self.videos = mommy.make(
            'Video',
            titulo='titulo_teste',
            _quantity=50,
            campus_origem=mommy.make('Campus'),
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        for i in self.videos:
            i.sites.add(self.site)

        # trecho cria um novo site e novos videos para simular o ambiente real
        self.site2 = mommy.make('Site', domain='cba.ifmt.dev')
        self.videos = mommy.make(
            'Video',
            titulo='titulo_teste',
            _quantity=10,
            campus_origem=mommy.make('Campus', slug='campus2'),
        )
        for i in self.videos:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('conteudo:videos_lista'), SERVER_NAME='rtr.ifmt.dev')

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
        HTML deve conter o 40 titulos,(20 para titulo da noticia, 20 para o alt da imagem)
        que e a quantidade para paginacao
        """
        self.assertContains(self.resp, 'titulo_teste', 40)


class GaleriaDetalheTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(
            'Galeria',
            titulo='titulo_teste',
            texto=u'texto_teste',
            data_publicacao='2014-06-05T10:16:00-04:00',
            publicado=True,
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        self.obj.tags.add('ifmt-teste')
        # as views de detalhe nao precisam de um site para ser exibida, para permitir o relacionamento entre
        # os conteudos dos sites
        # self.galeria.sites.add(self.site)

        self.resp = self.client.get(reverse('conteudo:galeria_detalhe',
                                            kwargs={'slug': self.obj.slug}), SERVER_NAME='rtr.ifmt.dev')

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
        self.assertContains(self.resp, 'ifmt-teste')


class GaleriaListaTest(TestCase):
    def setUp(self):
        self.galerias = mommy.make(
            'Galeria',
            titulo='titulo_teste',
            _quantity=50,
            campus_origem=mommy.make('Campus', slug='campus1'),
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')

        for i in self.galerias:
            i.sites.add(self.site)

        # trecho cria um novo site e novas galerias para simular o ambiente real
        self.site2 = mommy.make('Site', domain='cba.ifmt.dev')
        self.galerias = mommy.make(
            'Galeria',
            titulo='titulo_teste',
            _quantity=10,
            campus_origem=mommy.make('Campus', slug='campus2'),
        )
        for i in self.galerias:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('conteudo:galerias_lista'), SERVER_NAME='rtr.ifmt.dev')

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


class TagListaTest(TestCase):
    def setUp(self):
        self.eventos = mommy.make(
            'Evento',
            titulo='titulo_teste',
            _quantity=21,
            campus_origem=mommy.make('Campus')
        )
        self.site = mommy.make('Site', domain='rtr.ifmt.dev')

        for evento in self.eventos:
            evento.tags.add('ifmt-teste')
            evento.sites.add(self.site)
            evento.save()

        self.resp = self.client.get(reverse('conteudo:tags_lista', args=[],
                                            kwargs={'slug': 'ifmt-teste'}), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET /conteudo/galerias/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Eventos lista deve renderizar o template lista.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/tag_lista.html')

    def test_html(self):
        """
        HTML deve conter o 1 tag
        """
        self.assertContains(self.resp, 'ifmt-teste', 1)

    def test_listagem(self):
        """
        HTML de listagem deve conter o 20 (numero de paginacao) eventos (modelo base)
        """
        self.assertContains(self.resp, 'titulo_teste', 20)