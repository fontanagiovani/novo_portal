# -*- coding: utf-8 -*-
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from portal.core.models import MenuContainer
from portal.core.forms import MenuContainerForm


class MenuContainerTest(TestCase):
    def setUp(self):
        self.obj = MenuContainer(
            nome='MENU1'
        )

    def test_de_criacao(self):
        'MenuContainer deve ter nome'
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_nome_nao_poder_ser_null(self):
        'O campo nome nao pode ser nulo'
        self.obj.nome = None
        self.assertRaises(IntegrityError, self.obj.save)

    def test_nome_nao_pode_ser_blank(self):
        'O campo nome nao pode ser vazio'
        data = {'nome': ''}
        form = MenuContainerForm(data)
        form.is_valid()
        self.assertItemsEqual(['nome'], form.errors)

    def test_unicode(self):
        'Testa se unicode eh valido'
        self.assertEqual('MENU1', unicode(self.obj))