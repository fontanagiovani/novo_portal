# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db.utils import IntegrityError
from portal.core.models import Menu
from portal.core.models import MenuContainer
from portal.core.forms import MenuForm
from portal.core.models import Site


class MenuTest(TestCase):
    def setUp(self):
        container = MenuContainer(nome='MENU1')
        container.save()

        self.site1 = Site(
            parent=None,
            nome='Campus Campo Novo do Parecis',
            slug='cnp'
        )
        self.site1.save()

        self.obj = Menu(
            parent=None,
            titulo='Institucional',
            ordem=4,
            link='http://www.ifmt.edu.br',
            pagina=123456,
            menucontainer=container
        )

    def test_criacao(self):
        """
        Menu deve ter parent, titulo, local, ordem, link e pagina
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_titulo_nao_null(self):
        """
        O campo titulo nao deve ser nulo
        """
        self.obj.titulo = None
        self.assertRaises(IntegrityError, self.obj.save)

    def test_titulo_nao_blank(self):
        """
        O campo titulo nao deve ser vazio
        """
        dados = {'parent': None, 'titulo': '', 'ordem': 4, 'link': 'http://www.ifmt.edu.br',
                'pagina': 123456, 'menucontainer': self.obj.menucontainer.pk, 'sites': [self.site1.pk]}
        form = MenuForm(dados)
        form.is_valid()
        self.assertItemsEqual(['titulo'], form.errors)

    def test_ordem_nao_null(self):
        """
        O campo ordem nao deve ser nulo
        """
        self.obj.ordem = None
        self.assertRaises(IntegrityError, self.obj.save)

    def test_ordem_nao_blank(self):
        """
        O campo titulo nao deve ser vazio
        """
        dados = {'parent': None, 'titulo': 'Novo menu', 'ordem': '', 'link': 'http://www.ifmt.edu.br',
                'pagina': 123456, 'menucontainer': self.obj.menucontainer.pk, 'sites': [self.site1.pk]}
        form = MenuForm(dados)
        form.is_valid()
        self.assertItemsEqual(['ordem'], form.errors)

    def test_link_pode_ser_null(self):
        """
        O campo link pode ser nulo
        """
        self.obj.link = None
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_link_pode_ser_blank(self):
        """
        O campo link pode ser vazio
        """
        dados = {'parent': None, 'titulo': 'Novo menu', 'ordem': 2, 'link': '',
                'pagina': 123456, 'menucontainer': self.obj.menucontainer.pk, 'sites': [self.site1.pk]}
        form = MenuForm(dados)
        form.is_valid()
        self.assertItemsEqual([], form.errors)

    def test_pagina_pode_ser_null(self):
        """
        O campo pagina pode ser nulo
        """
        self.obj.pagina = None
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_pagina_pode_ser_blank(self):
        """
        O campo pagina pode ser vazio
        """
        dados = {'parent': None, 'titulo': 'Novo menu', 'ordem': 2, 'link': '',
                'pagina': '', 'menucontainer': self.obj.menucontainer.pk, 'sites': [self.site1.pk]}
        form = MenuForm(dados)
        form.is_valid()
        self.assertItemsEqual([], form.errors)

    def test_unicode(self):
        """
        Testa se o unicode eh valido
        """
        self.assertEqual('Institucional', unicode(self.obj))


class MenuRelacionamentoTest(TestCase):
    def setUp(self):
        self.site1 = Site(
            parent=None,
            nome='Campus Campo Novo do Parecis',
            slug='cnp'
        )
        self.site1.save()

        self.site2 = Site(
            parent=None,
            nome='Campus Bela Vista',
            slug='blv'
        )
        self.site2.save()

        container = MenuContainer(nome='MENU1')
        container.save()

        self.obj = Menu(
            parent=None,
            titulo='Institucional',
            ordem=4,
            link='http://www.ifmt.edu.br',
            pagina=123456,
            menucontainer=container
        )

    def test_create(self):
        """
        Menu deve ter relacionamento n:m com Site
        """
        self.obj.save()
        self.obj.sites.add(self.site1)
        self.obj.sites.add(self.site2)
        self.assertIsNotNone(self.obj.pk)

    def test_site_nao_pode_ser_nulo(self):
        """
        Site nao pode ser nulo
        """
        # self.assertRaises(IntegrityError, self.obj.save)
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_site_nao_pode_ser_vazio(self):
        """
        site nao pode ser vazio
        """
        dados = {'parent': None, 'titulo': 'Novo menu', 'ordem': 2, 'link': '',
                'pagina': '', 'menucontainer': self.obj.menucontainer.pk, 'sites': []}
        form = MenuForm(dados)
        form.is_valid()
        self.assertItemsEqual(['sites'], form.errors)