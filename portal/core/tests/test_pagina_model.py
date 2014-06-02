# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from portal.core.models import Conteudo
from portal.core.models import Site


class PaginaTest(TestCase):
    def setUp(self):
        self.site = Site(
            parent=None,
            nome=u'Campus Cuiabá',
            slug='cba',
        )
        self.site.save()

        self.obj = Conteudo(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_postagem=timezone.now(),  # '2014-03-21 17:59:00',
        )

    def test_criacao(self):
        """
        pagina deve conter titulo, texto, data_postagem
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_relacionamento_site(self):
        """
        Site nao pode ser nulo
        """
        self.obj.save()
        self.obj.sites.add(self.site)
        self.assertEqual(1, self.obj.sites.count())

    def test_unicode(self):
        """
        Pagina deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))