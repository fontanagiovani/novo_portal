#coding: utf-8

from django.test import TestCase
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from django.core.urlresolvers import reverse
from filer.models import Image
from django.core.files import File
from model_mommy import mommy


class HomeBannerContextTest(TestCase):
    def setUp(self):
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagemBanner'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

        self.banner = mommy.make(Banner, _quantity=3, arquivo=midia_image)
        self.resp = self.client.get(reverse('home'))

    def test_banner(self):
        """
         A Home deve conter três banners
        """
        self.assertContains(self.resp, u'imagembanner', 3)


class HomeAcessoRapidoContextTest(TestCase):
    def setUp(self):
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagemAcessoRapido'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

        self.banner = mommy.make(BannerAcessoRapido, _quantity=5, titulo=u'Titulo do banner acesso rapido', midia_image=midia_image)
        self.resp = self.client.get(reverse('home'))

    def test_banner(self):
        """
         Acesso rápido deve conter cinco banners
        """
        self.assertContains(self.resp, u'Titulo do banner acesso rapido', 5)

