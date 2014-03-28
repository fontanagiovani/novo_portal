# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from portal.core.models import Site


class SiteModelTest(TestCase):

    def setUp(self):
        self.obj = Site(
            nome='Campus Cuiabá',
            slug='campus-cuiaba',
        )

    def test_de_criacao(self):
        'Site deve ter parent, nome e slug'
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        'testa se unicode eh valido'
        self.assertEqual('campus-cuiaba', unicode(self.obj))