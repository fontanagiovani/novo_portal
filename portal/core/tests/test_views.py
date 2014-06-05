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
        # ordenacao por data e id decrescente
        mommy.make(Conteudo, _quantity=4, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Conteudo, _quantity=7, titulo=u'test1')
        mommy.make(Conteudo, _quantity=4, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Conteudo, _quantity=5, titulo=u'test1')
        self.resp = self.client.get(reverse('home'))

    def test_conteudo_mais_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque
        """
        # Sao esperados 8 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        # Como e feita a exibicao do titulo como alt da tag img esse numero duplica, ficando 16
        self.assertContains(self.resp, u'test1', 8)

    def test_conteudo_noticias_destaque(self):
        """
        A home de conter noticias de destaque no topo e pode tambem existir na listagem
        """
        # Sao esperados 5 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        # Como sao exibidos os thumbnails para navegacao esse numero duplica, ficando 10
        # Como e feita a exibicao do titulo como alt da tag img esse numero duplica, ficando 20
        self.assertContains(self.resp, u'noticia_destaque', 10)
