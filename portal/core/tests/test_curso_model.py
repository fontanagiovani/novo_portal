# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from portal.core.models import Curso
from portal.core.forms import CursoForm


class CursoModelTest(TestCase):

    def setUp(self):
        self.obj = Curso(
            campus=u'CNP',
            nivel=u'SUP',
            nome=u'Curso Superior de Bacharelado em Engenharia Florestal',
            descricao=u'Descrição do curso',)

    def test_de_criacao(self):
        'Curso deve ter campus, nivel, nome e descricao'
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    if not settings.DATABASES.get('default').get('ENGINE').__contains__('sqlite3'):
        def test_campus_tamanho_maximo(self):
            'O Campus deve possuir no maximo 3 caracters'
            curso = Curso(
                campus='ABCD',
                nivel=u'SUP',
                nome=u'Curso Superior de Bacharelado em Engenharia Florestal',
                descricao=u'Descrição do curso',)

            self.assertRaises(DataError, curso.save)

    def test_descricao_blank(self):
        'descrição pode ser vazia'
        dados = {'campus': 'CNP', 'nivel': 'SUP', 'nome': 'Curso Superior de Bacharelado em Engenharia Florestal', 'descricao': ''}
        form = CursoForm(dados)
        form.is_valid()
        self.assertItemsEqual([], form.errors)

    def test_descricao_null(self):
        'descrição pode ser nula'
        self.obj.descricao = None
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_valor_diferente_choice(self):
        'erro caso tente inserir valor diferente do choice'
        dados = {'campus': 'ABC', 'nivel': 'XYZ', 'nome': 'Curso Superior de Bacharelado em Engenharia Florestal', 'descricao': ''}
        form = CursoForm(dados)
        form.is_valid()
        self.assertItemsEqual(['campus', 'nivel'], form.errors)

    def test_nome_requerido(self):
        'campo nome nao pode ser vazio'
        dados = {'campus': 'CNP', 'nivel': 'SUP', 'nome': '', 'descricao': ''}
        form = CursoForm(dados)
        form.is_valid()
        self.assertItemsEqual(['nome'], form.errors)

    def test_nome_nao_null(self):
        'nome nao pode ser nulo'
        self.obj.nome = None
        self.assertRaises(IntegrityError, self.obj.save)

    def test_unicode(self):
        'testa se unicode eh valido'
        self.assertEqual(u'CNP - Curso Superior de Bacharelado em Engenharia Florestal', unicode(self.obj))