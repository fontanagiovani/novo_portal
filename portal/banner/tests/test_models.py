#coding: utf-8
from django.test.testcases import TestCase
from django.conf import settings
from django.utils import timezone
from django.core.files import File
from filer.models import Image

from portal.banner.models import Banner
from portal.core.tests.util import del_midia_filer


class BannerTest(TestCase):
    def setUp(self):
        self.img_path = settings.BASE_DIR + '/portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.banner = Banner(
            titulo=u'BannerTesteTitulo',
            data_publicacao=timezone.now(),
            arquivo=midia_image,
            publicado=True,
            tipo=1,
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

    def test_esta_publicado(self):
        """
        Testa se um banner esta publicado ou nao. A condicao para que um banner seja considerado como publicado e que
        esteja marcado como publicado e a data de publicacao seja anterior a data atual
        """
        # data de 1 dia antes de hoje
        self.banner.data_publicacao = timezone.now() - timezone.timedelta(days=1)
        self.banner.publicado = True
        self.assertTrue(self.banner.esta_publicado)

        self.banner.publicado = False
        self.assertFalse(self.banner.esta_publicado)

        # data de 1 dia depois de hoje
        self.banner.data_publicacao = timezone.now() + timezone.timedelta(days=1)
        self.banner.publicado = True
        self.assertFalse(self.banner.esta_publicado)

        # data de 1 dia antes de hoje
        self.banner.data_publicacao = timezone.now() - timezone.timedelta(days=1)
        self.banner.publicado = False
        self.assertFalse(self.banner.esta_publicado)

    def tearDown(self):
        del_midia_filer(self.img_name)
