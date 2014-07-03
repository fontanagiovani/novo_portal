# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from portal.core.models import Conteudo
from portal.conteudo.models import Noticia


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
        self.conteudo_evento = mommy.make(Conteudo, _quantity=3, titulo=u'Titulo do evento', tipo='EVENTO')
        self.conteudo_banner = mommy.make(Conteudo, _quantity=3, titulo=u'Titulo do banner', tipo='BANNER')
        self.resp = self.client.get(reverse('home'))

    def test_conteudo_mais_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque
        """
        # Sao esperados 9 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'test1', 9)

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


class ConteudoDetalheTest(TestCase):
    def setUp(self):
        self.conteudo = mommy.make(Conteudo,
                                   titulo='titulo_teste',
                                   texto=u'texto_teste',
                                   data_publicacao='2014-06-05 10:16:00'
                                   )
        self.resp = self.client.get(reverse('conteudo_detalhe', kwargs={'conteudo_id': self.conteudo.id}))

    def test_get(self):
        """
        GET /conteudo/1/ deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Conteudo detalhe deve renderizar o template conteudo.html
        """
        self.assertTemplateUsed(self.resp, 'core/conteudo.html')

    def test_html(self):
        """
        HTML deve conter o titulo, data, texto
        """
        self.assertContains(self.resp, 'titulo_teste')
        self.assertContains(self.resp, u'texto_teste')
        self.assertContains(self.resp, u'5 de Junho de 2014 às 10:16')