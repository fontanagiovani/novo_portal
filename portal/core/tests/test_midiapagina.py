# -*- coding: utf-8 -*-
from django.core.files.base import File
from django.utils import timezone
from django.test import TestCase
from pkg_resources import StringIO
from portal.core.models import MidiaPagina
from portal.core.models import Pagina


class MidiaPaginaTest(TestCase):
    def setUp(self):
        # Gera o arquivo na memoria
        arquivo_temp = StringIO()
        arquivo_temp.write('Ola... teste')

        arquivo = File(arquivo_temp, name='teste.txt')

        self.pagina = Pagina(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_postagem=timezone.now()  # '2014-03-21 17:59:00',
        )

        self.pagina.save()

        self.obj = MidiaPagina(
            pagina=self.pagina,
            descricao=u'Amostra de midia',
            arquivo=arquivo
        )

    def test_criacao(self):
        """
        Midia deve possuir descricao e arquivo
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

        # Deleta o arquivo gerado
        self.obj.arquivo.delete()

    def test_unicode(self):
        """
        Midia deve apresentar a descricao como unicode
        """
        self.assertEqual(u'Amostra de midia', unicode(self.obj))