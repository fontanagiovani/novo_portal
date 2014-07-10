#coding: utf-8
from django.test.testcases import TestCase
from portal.banner.models import Banner
from django.core.files import File
from filer.models import Image
from portal.banner.models import BannerAcessoRapido
from django.utils import timezone


class BannerTest(TestCase):
    def setUp(self):
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagemBanner'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

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
            Banner deve apresentar o nome da midia como unicode
        """
        self.assertEqual(u'BannerTesteTitulo', unicode(self.banner))

#
# class AcessoRapidoTest(TestCase):
#     def setUp(self):
#         midia_image = FilerImageField(name='bannerAcessoRapido')
#         # midia_image.save()
#
#         self.banner = BannerAcessoRapido(
#             titulo=u'Titulo Banner Acesso Rapido',
#             data_publicacao=timezone.now(),
#             midia_image=midia_image,
#
#         )
#
#     def test_criacao(self):
#         """
#             Banner de acesso rapido deve conter título, data de publicacao e arquivo de imagem
#         """
#         self.banner.save()
#         self.assertIsNotNone(self.banner.pk)