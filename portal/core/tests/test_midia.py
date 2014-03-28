# -*- coding: utf-8 -*-
from django.core.files.base import File
from django.test import TestCase
from pkg_resources import StringIO
from portal.core.models import Midia


class MidiaTest(TestCase):
    def setUp(self):
        # Gera o arquivo na memoria
        arquivo_temp = StringIO()
        arquivo_temp.write('Ola... teste')

        arquivo = File(arquivo_temp, name='teste.txt')

        self.obj = Midia(
            descricao=u'Amostra de midia',
            arquivo=arquivo
        )

    def test_criacao(self):
        """
        Midia deve possuir descricao e arquivo
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

        # Deleta o arquivo gravado no disco
        self.obj.delete()

    def test_unicode(self):
        """
        Midia deve apresentar a descricao como unicode
        """
        self.assertEqual(u'Amostra de midia', unicode(self.obj))