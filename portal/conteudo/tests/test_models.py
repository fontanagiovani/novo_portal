# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.utils import timezone
from filer.models import Image
from filer.models import File as FileFiler
from model_mommy import mommy

from portal.core.tests.util import del_midia_filer


class ConteudoTest(TestCase):
    def setUp(self):
        self.obj = mommy.prepare('Conteudo', titulo=u'Título', campus_origem=mommy.make('Campus'))

    def test_criacao(self):
        """
        Noticia deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_esta_publicado(self):
        """
        Conteudo para estar publicado deve estar marcado como publicado e tambem possuir data de publicacao
        posterior a data atual
        """
        self.obj.data_publicacao = timezone.now() - timezone.timedelta(days=1)
        self.obj.publicado = True
        self.assertTrue(self.obj.esta_publicado)

        self.obj.publicado = False
        self.assertFalse(self.obj.esta_publicado)

        self.obj.data_publicacao = timezone.now() + timezone.timedelta(days=1)
        self.obj.publicado = True
        self.assertFalse(self.obj.esta_publicado)

        self.obj.data_publicacao = timezone.now() - timezone.timedelta(days=1)
        self.obj.publicado = False
        self.assertFalse(self.obj.esta_publicado)


class NoticiaTest(TestCase):
    def setUp(self):
        self.obj = mommy.prepare('Noticia', titulo=u'Título', campus_origem=mommy.make('Campus'))

    def test_criacao(self):
        """
        Noticia deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_get_absolute_url(self):
        """
        Noticia deve ter um url de acesso direto
        """
        self.obj.save()
        self.assertEqual(reverse('conteudo:noticia_detalhe', kwargs={'slug': self.obj.slug}),
                         self.obj.get_absolute_url())


class AnexoTest(TestCase):
    def setUp(self):
        self.obj = mommy.make('Conteudo', titulo=u'Título', campus_origem=mommy.make('Campus'))

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.anexo = mommy.prepare('Anexo', conteudo=self.obj, descricao=u'foto1', arquivo=midia_image)

    def test_criacao(self):
        """
        Anexo deve possuir conteudo, descricao e arquivo
        """
        self.anexo.save()
        self.assertIsNotNone(self.anexo.pk)

    def test_unicode(self):
        """
        Anexo deve apresentar descricao como unicode
        """
        self.assertEqual(u'foto1', unicode(self.anexo))


class PaginaTest(TestCase):
    def setUp(self):
        self.obj = mommy.prepare('Pagina', titulo=u'Título', campus_origem=mommy.make('Campus'))

    def test_criacao(self):
        """
        Pagina deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_get_absolute_url(self):
        """
        Noticia deve ter um url de acesso direto
        """
        self.obj.save()
        self.assertEqual(reverse('conteudo:pagina_detalhe', kwargs={'slug': self.obj.slug}),
                         self.obj.get_absolute_url())


class EventoTest(TestCase):
    def setUp(self):
        self.obj = mommy.prepare('Evento', titulo=u'Título', campus_origem=mommy.make('Campus'))

    def test_criacao(self):
        """
        Evento deve conter titulo, texto, data_publicacao, data_inicio e data_fim
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Evento deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_get_absolute_url(self):
        """
        Evento deve ter um url de acesso direto
        """
        self.obj.save()
        self.assertEqual(reverse('conteudo:evento_detalhe', kwargs={'slug': self.obj.slug}),
                         self.obj.get_absolute_url())


class VideoTest(TestCase):
    def setUp(self):
        self.obj = mommy.prepare('Video', titulo=u'Título', campus_origem=mommy.make('Campus'))

    def test_criacao(self):
        """
        Video deve conter titulo,Id do Video, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Video deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_get_absolute_url(self):
        """
        Video deve ter um url de acesso direto
        """
        self.obj.save()
        self.assertEqual(reverse('conteudo:video_detalhe', kwargs={'slug': self.obj.slug}),
                         self.obj.get_absolute_url())


class GaleriaTest(TestCase):
    def setUp(self):
        self.obj = mommy.prepare('Galeria', titulo=u'Título', campus_origem=mommy.make('Campus'))

    def test_criacao(self):
        """
        Galeria deve conter titulo,texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Galeria deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_get_absolute_url(self):
        """
        Galeria deve ter um url de acesso direto
        """
        self.obj.save()
        self.assertEqual(reverse('conteudo:galeria_detalhe', kwargs={'slug': self.obj.slug}),
                         self.obj.get_absolute_url())


class ImagemGaleriaTest(TestCase):
    def setUp(self):
        self.obj = mommy.make('Galeria', titulo=u'Título', campus_origem=mommy.make('Campus'))

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.anexo = mommy.prepare('ImagemGaleria', galeria=self.obj, descricao=u'foto1', imagem=midia_image)

    def test_criacao(self):
        """
        Anexo deve possuir descricao e Imagem
        """
        self.anexo.save()
        self.assertIsNotNone(self.anexo.pk)

    def test_unicode(self):
        """
        Anexo deve apresentar descricao como unicode
        """
        self.assertEqual(u'foto1', unicode(self.anexo))

    def tearDown(self):
        del_midia_filer(self.img_name)


class LiciatacaoTest(TestCase):
    def setUp(self):
        campus_origem = mommy.make('Campus')
        self.obj = mommy.prepare('Licitacao', titulo=u'Título', publicado=True, campus_origem=campus_origem)

    def test_criacao(self):
        """
        Noticia deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

    def test_esta_publicado(self):
        """
        Conteudo para estar publicado deve estar marcado como publicado e tambem possuir data de publicacao
        posterior a data atual
        """
        self.obj.data_publicacao = timezone.now() - timezone.timedelta(days=1)
        self.obj.publicado = True
        self.assertTrue(self.obj.esta_publicado)

        self.obj.publicado = False
        self.assertFalse(self.obj.esta_publicado)

        self.obj.data_publicacao = timezone.now() + timezone.timedelta(days=1)
        self.obj.publicado = True
        self.assertFalse(self.obj.esta_publicado)

        self.obj.data_publicacao = timezone.now() - timezone.timedelta(days=1)
        self.obj.publicado = False
        self.assertFalse(self.obj.esta_publicado)