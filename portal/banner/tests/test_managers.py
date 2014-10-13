# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from django.core.files import File
from model_mommy import mommy
from filer.models import Image

from portal.banner.models import Banner, BannerAcessoRapido


class BannerManagerTest(TestCase):
    def setUp(self):
        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            arquivo = Image.objects.create(original_filename=self.img_name, file=file_obj)

        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('Banner', _quantity=2, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_passada, arquivo=arquivo, publicado=False)

        mommy.make('Banner', _quantity=3, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_passada, arquivo=arquivo, publicado=True)

        mommy.make('Banner', _quantity=4, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_futura, arquivo=arquivo, publicado=False)

        mommy.make('Banner', _quantity=1, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_futura, arquivo=arquivo, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = Banner.publicados.all().count()
        self.assertEqual(qtd_registros, 3)


class BannerARManagerTest(TestCase):
    def setUp(self):
        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            arquivo = Image.objects.create(original_filename=self.img_name, file=file_obj)

        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)
        mommy.make('BannerAcessoRapido', _quantity=2, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_passada, arquivo=arquivo, publicado=False)

        mommy.make('BannerAcessoRapido', _quantity=3, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_passada, arquivo=arquivo, publicado=True)

        mommy.make('BannerAcessoRapido', _quantity=4, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_futura, arquivo=arquivo, publicado=False)

        mommy.make('BannerAcessoRapido', _quantity=1, titulo=u'BannerTesteTitulo',
                   data_publicacao=data_futura, arquivo=arquivo, publicado=True)

    def test_publicados(self):
        """
        O manager publicados deve retornar somente os registros que estao marcados como publicados e com data
        de publicacao anterior a data atual
        """
        qtd_registros = BannerAcessoRapido.publicados.all().count()
        self.assertEqual(qtd_registros, 3)