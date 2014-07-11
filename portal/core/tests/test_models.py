# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from portal.core.models import Selecao
from django.core.files import File
from filer.models import Image
from filer.models import File as FileFiler
from django.core.urlresolvers import reverse
from model_mommy import mommy


class SelecaoTest(TestCase):
    def setUp(self):
        self.obj = Selecao(
            status = 'AND',
            tipo = 'AMBS',
            titulo=u'Título',
            url=u'Url de destino',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
            data_abertura_edital = timezone.now(),  # '2014-03-21 17:59:00',
            data_abertura_inscricoes = timezone.now(),  # '2014-03-21 17:59:00',
            data_encerramento_inscricoes = timezone.now(),  # '2014-03-21 17:59:00',
        )

    def test_criacao(self):
        """
        Video deve conter status,tipo, titulo,url, data de punlicação, abertura de edital, de incrições e encerramento de inscrições
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Video deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))



