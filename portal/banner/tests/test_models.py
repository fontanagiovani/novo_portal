#coding: utf-8
from django.test.testcases import TestCase
from portal.banner.models import Banner
from portal.banner.models import BannerAcessoRapido
from filer.models import File as FileFiler
from django.utils import timezone


class BannerTest(TestCase):
    def setUp(self):
        arquivo = FileFiler(name='midiaBanner01')
        arquivo.save()

        self.banner = Banner(
            data_publicacao=timezone.now(),
            arquivo=arquivo,
        )

    def test_criacao(self):
        """
            Banner deve possuir data de publicacao e arquivo(midia)
        """
        self.banner.save()
        self.assertIsNotNone(self.banner.pk)

    def test_unicode(self):
        """
            Banner deve apresentar o nome do arquivo como unicode
        """
        self.assertEqual(u'midiaBanner01', unicode(self.banner))

    def test_tituloNulo(self):
        """
            O titulo nao pode ser nulo
        """
        self.banner.titulo=u'tituloBanner01'
        self.banner.save()
        self.assertEqual(1, self.banner.pk)

class AcessoRapidoTest(TestCase):
    def setUp(self):
        arquivo = FileFiler(name='bannerAcessoRapido')
        arquivo.save()

        self.banner = BannerAcessoRapido(
            titulo=u'Titulo Banner Acesso Rapido',
            data_publicacao=timezone.now(),
            midia_image=arquivo,

        )

    def test_criacao(self):
        """
            Banner de acesso rapido deve conter título, data de publicacao e arquivo de imagem
        """
        self.banner.save()
        self.assertIsNotNone(self.banner.pk)