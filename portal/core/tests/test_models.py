# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.sites.models import Site
from django.utils import timezone
from portal.core.models import Menu
from portal.core.models import Selecao, TipoSelecao
from model_mommy import mommy


class TipoSelecaoTest(TestCase):
    def setUp(self):
        self.obj = TipoSelecao(
            parent=None,
            titulo=u'Título',
            slug='titulo'
        )

    def test_criacao(self):
        """
        Video deve conter parent, titulo,Slug,
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Video deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))


class SelecaoTest(TestCase):
    def setUp(self):
        self.tipo = TipoSelecao(
            parent=None,
            titulo=u'Título',
            slug='titulo'
        )
        self.tipo.save()

        self.obj = Selecao(
            status='AND',
            titulo=u'Título',
            tipo=self.tipo,
            url=u'Url de destino',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
            data_abertura_edital=timezone.now(),  # '2014-03-21 17:59:00',
            data_abertura_inscricoes=timezone.now(),  # '2014-03-21 17:59:00',
            data_encerramento_inscricoes=timezone.now(),  # '2014-03-21 17:59:00',
        )

    def test_criacao(self):
        """
        Video deve conter status,tipo, titulo,url, data de punlicação, abertura de edital, de incrições e encerramento de inscrições
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Video deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))


class MenuTest(TestCase):
    def setUp(self):
        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]
        self.menu = Menu(
            parent=None,
            titulo=u'TituloMenu',
            slug=u'menu-slug',
            url=u'http.www.menuteste@url.com',
            ordem=1,
            site=self.site
        )

    def test_criacao(self):
        """
        Menu deve conter titulo, slug e url
        """
        self.menu.save()
        self.assertIsNotNone(self.menu.pk)

    def test_unicode(self):
        """
        Menu deve apresentar o titulo como unicode
        """
        self.assertEqual(u'TituloMenu', unicode(self.menu))


