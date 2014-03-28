# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase


class CursoTest(TestCase):

    def setUp(self):
        self.resp = self.client.get(reverse('home'))

    def test_get(self):
        'GET / must return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Response should be a rendered template.'
        self.assertTemplateUsed(self.resp, 'core/base.html')