#coding: utf-8

from django.test import TestCase
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from django.core.urlresolvers import reverse
from filer.models import Image
from django.core.files import File
from model_mommy import mommy
import os
import shutil


class HomeBannerContextTest(TestCase):
    def setUp(self):
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagembanner'
        with open(img_path) as self.img:
            self.file_obj = File(self.img, name=img_name)
            self.midia_image = Image.objects.create(original_filename=img_name, file=self.file_obj)

            #codigo de teste
        with open(img_path) as self.imgteste:
            self.file_obj = File(self.imgteste, name='testeimagem')
            self.midia_image_teste = Image.objects.create(original_filename=img_name, file=self.file_obj)

        self.banner = mommy.make(Banner, _quantity=3, arquivo=self.midia_image)
        self.resp = self.client.get(reverse('home'))

    def test_banner(self):
        """
         A Home deve conter três banners
        """
        self.assertContains(self.resp, u'imagembanner', 3)

    def tearDown(self):
        # for root, dirs, files in os.walk('/home/raquelmelo/novo_portal/media/filer_public', topdown=False):
        #         for name in dirs:
        #             print(os.path.join(root, name))
        #             shutil.rmtree(os.path.join(root, name))
        #         for name in files:
        #             if name.startswith('imagembanner'):
        #                 print(os.path.join(root, name))
        #                 os.remove(os.path.join(root, name))
        #                 os.remove(root)

                    # os.rmdir(os.path.join(root, name))
                    # if os.path.exists(os.path.join(name, 'imagembanner')):
                    #     shutil.rmtree(os.path.join(root, name))
            # for name in dirs:
            #     if os.path.exists(os.path.join(name, 'imagembanner')):
            #         os.remove(os.path.join(name, 'imagembanner'))
            #         os.rmdir(os.path.join(root, name))

        for root, dirs, files in os.walk('/home/raquelmelo/novo_portal/media/filer_public_thumbnails', topdown=False):
            for name in files:
                if name.startswith('imagembanner'):
                    print(os.path.join(root, name))
                    print(os.path.join(root))
                    os.remove(os.path.join(root, name))
                    os.rmdir(os.path.join(root))
            #
            # for name in dirs:
            #     if os.listdir(os.path.join(root, name)) == "":
            #         print(os.path.join(root, name))
            #         # print(os.path.join(root))
            #         # os.rmdir(os.path.join(root, name))
            #         shutil.rmtree(os.path.join(root, name))
            #         # shutil.rmtree(os.path.join(root))

class HomeAcessoRapidoContextTest(TestCase):
    def setUp(self):
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagemacessorapido'
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

