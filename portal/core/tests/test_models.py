# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from portal.core.models import Conteudo
from portal.core.models import Midia
from filer.models import File as FileFiler
from filer.models.imagemodels import Image
from model_mommy import mommy


class ConteudoTest(TestCase):
    def setUp(self):
        self.obj = Conteudo(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )

    def test_criacao(self):
        """
        conteudo deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Conteudo deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

class ConteudoMidiaTeste(TestCase):
    def setUp(self):
        self.conteudo = mommy.make(Conteudo, )

class MidiaTest(TestCase):
    def setUp(self):
        self.conteudo = Conteudo(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.conteudo.save()

        arquivo = FileFiler()
        arquivo.save()

        self.midia = Midia(
            conteudo=self.conteudo,
            descricao=u'foto1',
            arquivo=arquivo
        )

    def test_criacao(self):
        '''
        Midia deve possuir conteudo, descricao e arquivo
        '''
        self.midia.save()
        self.assertIsNotNone(self.midia.pk)


    def test_unicode(self):
        '''
        Midia deve apresentar descricao como unicode
        '''
        self.assertEqual(u'foto1', unicode(self.midia))

