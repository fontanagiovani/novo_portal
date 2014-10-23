# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.utils import timezone
from filer.models import Image
from model_mommy import mommy

from portal.banner.models import Banner
from portal.core.tests.util import del_midia_filer
from portal.core.models import Destino


class HomeBannerContextTest(TestCase):
    def setUp(self):
        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as self.img:
            self.file_obj = File(self.img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=self.file_obj)

        data_passada = timezone.now() - timezone.timedelta(days=1)
        data_futura = timezone.now() + timezone.timedelta(days=1)

        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner destaque publicado', tipo=1,
                   arquivo=midia_image, publicado=True, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner destaque nao publicado', tipo=1,
                   arquivo=midia_image, publicado=False, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner destaque publicado', tipo=1,
                   arquivo=midia_image, publicado=True, data_publicacao=data_futura)

        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner link de acesso publicado', tipo=2,
                   arquivo=midia_image, publicado=True, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner link de acesso nao publicado', tipo=2,
                   arquivo=midia_image, publicado=False, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner link de acesso publicado', tipo=2,
                   arquivo=midia_image, publicado=True, data_publicacao=data_futura)

        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner governamental publicado', tipo=3,
                   arquivo=midia_image, publicado=True, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner governamental nao publicado', tipo=3,
                   arquivo=midia_image, publicado=False, data_publicacao=data_passada)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner governamental publicado', tipo=3,
                   arquivo=midia_image, publicado=True, data_publicacao=data_futura)

        self.img_name = u'logo'
        with open(self.img_path) as self.img:
            self.file_obj = File(self.img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=self.file_obj)

        self.site = mommy.make('Site', domain='rtr.ifmt.dev')
        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

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
        self.assertContains(self.resp, u'Titulo do banner destaque publicado', 8)
        self.assertContains(self.resp, u'Titulo do banner link de acesso publicado', 10)

    def tearDown(self):
        del_midia_filer(self.img_name)
