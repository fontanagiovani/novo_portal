# coding: utf-8
from tempfile import _RandomNameSequence
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.core.models import Selecao, TipoSelecao, Menu
import random


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
        mommy.make(Noticia, _quantity=4, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=7, titulo=u'test1')
        mommy.make(Noticia, _quantity=4, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=5, titulo=u'test1')
        mommy.make(Evento, _quantity=3, titulo=u'Titulo do evento')
        self.resp = self.client.get(reverse('home'))

    def test_conteudo_mais_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque+
        """
        # Sao esperados 9 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'test1', 10)

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

    def test_conteudo_noticias_destaque(self):
        """
        A home de conter noticias de destaque no topo e pode tambem existir na listagem
        """
        # Sao esperados 5 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        # Como sao exibidos os thumbnails para navegacao esse numero duplica, ficando 10
        self.assertContains(self.resp, u'noticia_destaque', 10)


class SelecaoTest(TestCase):
    def setUp(self):
        self.tipo = TipoSelecao(
            parent=None,
            titulo=u'Título',
            slug='titulo'
        )
        self.tipo.save()
        self.selecao = mommy.make(Selecao, titulo='titulo_teste', tipo=self.tipo, _quantity=50)
        self.menuselecao = mommy.make(TipoSelecao, titulo=u'test1', _quantity=7)
        self.resp = self.client.get(reverse('selecao'))

    def test_get(self):
        """
        GET /selecao/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Eventos lista deve renderizar o template selecao_lista.html
        """
        self.assertTemplateUsed(self.resp, 'core/selecao_lista.html')

    def test_menu_selecao(self):
        self.assertContains(self.resp, u'test1', 7)


#Pesquisar sobre column unique no model.mommy
class Menutest(TestCase):
    def setUp(self):
        self.menu = mommy.make(Menu, titulo=u'TituloMenu', parent=None, _quantity=7, slug=_RandomNameSequence, ordem=random.randint(1, 100))
        self.resp = self.client.get(reverse('home'))

    def test_context_menu(self):
        """
        A home deve conter sete menus padrão
        """
        self.assertContains(self.resp, u'TituloMenu', 7)