# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from portal.core.models import Conteudo


class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('home'))


    def test_get(self):
        """
        GET / must return status code 200.
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Home must use template index.html
        """
        self.assertTemplateUsed(self.resp, 'core/base.html')


class HomeContextTest(TestCase):
    def setUp(self):
        self.conteudo = mommy.make(Conteudo, _quantity=8, titulo=u'Título do conteudo')
        self.conteudo_evento = mommy.make(Conteudo, _quantity=3, titulo=u'Titulo do evento', tipo='EVENTOS')
        self.conteudo_banner = mommy.make(Conteudo, _quantity=3, titulo=u'Titulo do banner', tipo='BANNER')
        self.resp = self.client.get(reverse('home'))

    def test_conteudo_noticias(self):
        """
        A home deve conter oito noticias
        """
        self.assertContains(self.resp, u'Título do conteudo', 8)

    def test_conteudo_evento(self):
        """
        A home deve conter tres eventos
        """

        self.assertContains(self.resp, u'Titulo do evento', 3)

    # def test_conteudo_banner(self):
    #     """
    #     A home deve conter tres conteudos do tipo banner
    #     """
    #     self.assertContains(self.resp, u'Titulo do banner', 3)

