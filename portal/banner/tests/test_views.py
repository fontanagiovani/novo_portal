#coding: utf-8

from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.files import File
from filer.models import Image
from model_mommy import mommy

from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from portal.core.tests.util import del_midia_filer
from portal.core.models import Template, SiteDetalhe


class HomeBannerContextTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as self.img:
            self.file_obj = File(self.img, name=self.img_name)
            self.midia_image = Image.objects.create(original_filename=self.img_name, file=self.file_obj)
        self.banner = mommy.make(Banner, _quantity=3, arquivo=self.midia_image)

        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]
        template = mommy.make(Template, descricao=Template.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make(SiteDetalhe, _quantity=1, template=template)[0]

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in Banner.objects.all():
            i.sites.add(self.site)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_banner(self):
        """
         A Home deve conter três banners
        """
        self.assertContains(self.resp, u'imagembanner', 3)

    def tearDown(self):
        del_midia_filer(self.img_name)


class HomeAcessoRapidoContextTest(TestCase):
    def setUp(self):
        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagemacessorapido'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.banner = mommy.make(BannerAcessoRapido, _quantity=5, titulo=u'Titulo do banner acesso rapido',
                                 midia_image=midia_image)

        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]
        template = mommy.make(Template, descricao=Template.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make(SiteDetalhe, _quantity=1, template=template)[0]

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in BannerAcessoRapido.objects.all():
            i.sites.add(self.site)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_banner(self):
        """
         Acesso rápido deve conter cinco banners (10 titulos devido o tooltip que tb exibe o titulo)
        """
        self.assertContains(self.resp, u'Titulo do banner acesso rapido', 10)

    def tearDown(self):
        del_midia_filer(self.img_name)