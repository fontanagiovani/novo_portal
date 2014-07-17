#coding: utf-8
from django.test.testcases import TestCase
from portal.banner.models import Banner
from django.core.files import File
from filer.models import Image
from portal.banner.models import BannerAcessoRapido
from django.utils import timezone
from portal.core.tests.util import del_midia_filer


class BannerTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.banner = Banner(
            titulo=u'BannerTesteTitulo',
            data_publicacao=timezone.now(),
            arquivo=midia_image,
        )

    def test_criacao(self):
        """
            Banner deve possuir titulo, data de publicacao e midia
        """
        self.banner.save()
        self.assertIsNotNone(self.banner.pk)

    def test_unicode(self):
        """
            Banner deve apresentar o titulo como unicode
        """
        self.assertEqual(u'BannerTesteTitulo', unicode(self.banner))

    def tearDown(self):
        del_midia_filer(self.img_name)
        import ipdb
        ipdb.set_trace()


class AcessoRapidoTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagemBanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.banner_acr = BannerAcessoRapido(
            titulo=u'Titulo Banner Acesso Rapido',
            data_publicacao=timezone.now(),
            midia_image=midia_image,

        )

    def test_criacao(self):
        """
            Banner de acesso rapido deve conter título, data de publicacao e arquivo de imagem
        """
        self.banner_acr.save()
        self.assertIsNotNone(self.banner_acr.pk)

    def test_unicode(self):
        """
            Banner de acesso rápido deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Titulo Banner Acesso Rapido', unicode(self.banner_acr))

    def tearDown(self):
        del_midia_filer(self.img_name)
        import ipdb
        ipdb.set_trace()