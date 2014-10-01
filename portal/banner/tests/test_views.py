# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.utils import timezone
from filer.models import Image
from model_mommy import mommy

from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from portal.core.tests.util import del_midia_filer
from portal.core.models import Destino


class HomeBannerContextTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as self.img:
            self.file_obj = File(self.img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=self.file_obj)

        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)

        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner publicado',
                   arquivo=midia_image, publicado=True, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner nao publicado',
                   arquivo=midia_image, publicado=False, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner publicado',
                   arquivo=midia_image, publicado=True, data_publicacao=data_futura)

        self.img_name = 'logo'
        with open(self.img_path) as self.img:
            self.file_obj = File(self.img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=self.file_obj)

        self.site = mommy.make('Site', _quantity=1, domain='rtr.ifmt.dev')[0]
        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make('SiteDetalhe', _quantity=1, destino=destino, logo=midia_image)[0]

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in Banner.publicados.all():
            i.sites.add(self.site)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_banner_publicados(self):
        """
         A Home deve conter três banners
        """
        # mesmo tendo 4 elementos somente o titulo aparece 2 vezes para cada banner (no tooltip e no modo small)
        self.assertContains(self.resp, u'Titulo do banner publicado', 8)

    def tearDown(self):
        del_midia_filer(self.img_name)


class HomeAcessoRapidoContextTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagemacessorapido'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)

        mommy.make('BannerAcessoRapido', _quantity=5, titulo=u'Titulo do banner acesso rapido publicado',
                   arquivo=midia_image, publicado=True, data_publicacao=data_passada)
        mommy.make('BannerAcessoRapido', _quantity=5, titulo=u'Titulo do banner acesso rapido não publicado',
                   arquivo=midia_image, publicado=False, data_publicacao=data_passada)
        mommy.make('BannerAcessoRapido', _quantity=5, titulo=u'Titulo do banner acesso rapido não publicado',
                   arquivo=midia_image, publicado=True, data_publicacao=data_futura)

        self.site = mommy.make('Site', _quantity=1, domain='rtr.ifmt.dev')[0]
        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make('SiteDetalhe', _quantity=1, destino=destino, logo=midia_image)[0]

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in BannerAcessoRapido.objects.all():
            i.sites.add(self.site)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_banner_publicados(self):
        """
         Acesso rápido deve conter cinco banners (10 titulos devido o tooltip que tb exibe o titulo)
        """
        # mesmo tendo 5 elementos somente o titulo aparece 2 vezes para cada banner (no tooltip e no modo small)
        self.assertContains(self.resp, u'Titulo do banner acesso rapido publicado', 10)

    def tearDown(self):
        del_midia_filer(self.img_name)