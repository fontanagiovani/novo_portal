#coding: utf-8

from django.test import TestCase
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from django.core.urlresolvers import reverse
from filer.models import Image
from django.core.files import File
from model_mommy import mommy
from portal.core.tests.util import del_midia_filer


class HomeBannerContextTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as self.img:
            self.file_obj = File(self.img, name=self.img_name)
            self.midia_image = Image.objects.create(original_filename=self.img_name, file=self.file_obj)
        self.banner = mommy.make(Banner, _quantity=3, arquivo=self.midia_image)
        self.resp = self.client.get(reverse('home'))

    def test_banner(self):
        """
         A Home deve conter três banners
        """
        self.assertContains(self.resp, u'imagembanner', 3)

    def tearDown(self):
        del_midia_filer(self.img_name)
        import ipdb
        ipdb.set_trace()


class HomeAcessoRapidoContextTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagemacessorapido'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.banner = mommy.make(BannerAcessoRapido, _quantity=5, titulo=u'Titulo do banner acesso rapido', midia_image=midia_image)
        self.resp = self.client.get(reverse('home'))

    def test_banner(self):
        """
         Acesso rápido deve conter cinco banners
        """
        self.assertContains(self.resp, u'Titulo do banner acesso rapido', 5)

    def tearDown(self):
        del_midia_filer(self.img_name)