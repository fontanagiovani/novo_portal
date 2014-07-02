# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from portal.conteudo.models import Noticia
from portal.conteudo.models import Anexo
from portal.conteudo.models import Pagina
from filer.models import File as FileFiler
from django.core.urlresolvers import reverse
from model_mommy import mommy


class NoticiaTest(TestCase):
    def setUp(self):
        self.obj = Noticia(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )

    def test_criacao(self):
        """
        Noticia deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_get_absolute_url(self):
        """
        Noticia deve ter um url de acesso direto
        """
        self.obj.save()
        self.assertEqual(reverse('noticia_detalhe', kwargs={'noticia_id': '1'}), self.obj.get_absolute_url())


class MidiaTest(TestCase):
    def setUp(self):
        self.noticia = Noticia(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.noticia.save()

        arquivo = FileFiler()
        arquivo.save()

        self.anexo = Anexo(
            noticia=self.noticia,
            descricao=u'foto1',
            arquivo=arquivo,
        )

    def test_criacao(self):
        """
        Anexo deve possuir conteudo, descricao e arquivo
        """
        self.anexo.save()
        self.assertIsNotNone(self.anexo.pk)

    def test_unicode(self):
        """
        Anexo deve apresentar descricao como unicode
        """
        self.assertEqual(u'foto1', unicode(self.anexo))


class PaginaTest(TestCase):
    def setUp(self):
        self.pagina = mommy.prepare(Pagina, titulo=u'Título')

    def test_criacao(self):
        """
        Pagina deve conter titulo, texto, data_publicacao
        """
        self.pagina.save()
        self.assertIsNotNone(self.pagina.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.pagina))

    def test_get_absolute_url(self):
        """
        Noticia deve ter um url de acesso direto
        """
        self.pagina.save()
        self.assertEqual(reverse('pagina_detalhe', kwargs={'pagina_id': '1'}), self.pagina.get_absolute_url())