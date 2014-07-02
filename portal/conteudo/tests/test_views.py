# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from portal.conteudo.models import Noticia


class NoticiaDetalheTest(TestCase):
    def setUp(self):
        self.noticia = mommy.make(Noticia,
                                  titulo='titulo_teste',
                                  texto=u'texto_teste',
                                  data_publicacao='2014-06-05 10:16:00')
        self.resp = self.client.get(reverse('conteudo:noticia_detalhe', kwargs={'noticia_id': self.noticia.id}))

    def test_get(self):
        """
        GET /noticia/1/ deve retorno status code 200
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
        GET /noticias/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Noticias lista deve renderizar o template lista.html
        """
        self.assertTemplateUsed(self.resp, 'conteudo/lista.html')

    def test_html(self):
        """
        HTML deve conter o 20 titulos, que e a quantidade para paginacao
        """
        self.assertContains(self.resp, 'titulo_teste', 20)