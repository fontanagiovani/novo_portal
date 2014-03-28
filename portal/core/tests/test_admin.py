# -*- coding: utf-8 -*-
from django.contrib import admin
from django.test import TestCase


class AdminRegisterTest(TestCase):

    def setUp(self):
        self.client.get('/')  # Usado para popular o admin.site._registry
        self.dicionario = str(admin.site.__dict__.values())

    def test_site(self):
        """
        site deve estar registrado no admin do django
        """
        self.assertTrue(self.dicionario.__contains__('portal.core.models.Site'))

    def test_menu(self):
        """
        menu deve estar registrado no admin do django
        """
        self.assertTrue(self.dicionario.__contains__('portal.core.models.Menu'))

    def test_curso(self):
        """
        curso deve estar registrado no admin do django
        """
        self.assertTrue(self.dicionario.__contains__('portal.core.models.Curso'))

    def test_pagina(self):
        """
        Pagina deve estar registrado no admin do django
        """
        self.assertTrue(self.dicionario.__contains__('portal.core.models.Pagina'))