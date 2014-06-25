from django.test import TestCase
from filer.models import File as FileFiler
from django.utils import timezone
from portal.banner.models import Banner

# Create your tests here.


class BannerTest(TestCase):
    def setUp(self):
        arquivo = FileFiler(name=u'banner1')
        arquivo.save()

        # import ipdb
        # ipdb.set_trace()

        self.banner = Banner(
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
            arquivo=arquivo
        )

    def test_criacao(self):
        """
        Banner deve possuir arquivo e data da publicacao
        """
        self.banner.save()
        self.assertIsNotNone(self.banner.pk)

    def test_unicode(self):
        """
         Banner deve apresentar descricao como unicode
        """
        self.assertEqual(u'banner1', unicode(self.banner))

