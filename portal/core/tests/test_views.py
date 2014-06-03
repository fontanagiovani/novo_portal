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
        self.conteudo = mommy.make(Conteudo, _quantity=8, titulo=u'test1')
        self.resp = self.client.get(reverse('home'))

    def test_conteudo_noticias(self):
        """
        A home deve conter oito noticias
        """
        self.assertContains(self.resp, u'test1', 8)

