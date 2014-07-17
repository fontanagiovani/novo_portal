# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from portal.conteudo.models import Noticia
from portal.conteudo.models import Pagina
from portal.conteudo.models import Evento
from portal.conteudo.models import Video
from portal.conteudo.models import Galeria
from portal.conteudo.models import ImagemGaleria
from portal.conteudo.models import AnexoNoticia
from portal.conteudo.models import AnexoPagina
from portal.conteudo.models import AnexoEvento
from django.core.files import File
from filer.models import Image
from filer.models import File as FileFiler
from django.core.urlresolvers import reverse
from model_mommy import mommy
from portal.core.tests.util import del_midia_filer


class NoticiaTest(TestCase):
    def setUp(self):
        self.obj = Noticia(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )

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
        self.assertEqual(reverse('conteudo:noticia_detalhe', kwargs={'noticia_id': self.obj.id}),
                         self.obj.get_absolute_url())


class AnexoNoticiaTest(TestCase):
    def setUp(self):
        self.noticia = Noticia(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.noticia.save()

        arquivo = FileFiler()
        arquivo.save()

        self.anexo = AnexoNoticia(
            noticia=self.noticia,
            descricao=u'foto1',
            arquivo=arquivo,
        )

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
        self.pagina = mommy.prepare(Pagina, titulo=u'Título')

    def test_criacao(self):
        """
        Pagina deve conter titulo, texto, data_publicacao
        """
        self.pagina.save()
        self.assertIsNotNone(self.pagina.pk)

    def test_unicode(self):
        """
        Noticia deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.pagina))

    def test_get_absolute_url(self):
        """
        Noticia deve ter um url de acesso direto
        """
        self.pagina.save()
        self.assertEqual(reverse('conteudo:pagina_detalhe', kwargs={'pagina_id': self.pagina.id}),
                         self.pagina.get_absolute_url())


class AnexoPaginaTest(TestCase):
    def setUp(self):
        self.pagina = Pagina(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.pagina.save()

        arquivo = FileFiler()
        arquivo.save()

        self.anexo = AnexoPagina(
            pagina=self.pagina,
            descricao=u'foto1',
            arquivo=arquivo,
        )

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


class EventoTest(TestCase):
    def setUp(self):
        self.obj = Evento(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
            data_inicio=timezone.now(),  # '2014-03-21 17:59:00',
            data_fim=timezone.now(),  # '2014-03-21 17:59:00',
        )

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
        self.assertEqual(reverse('conteudo:evento_detalhe', kwargs={'evento_id': self.obj.id}),
                         self.obj.get_absolute_url())


class AnexoEventoTest(TestCase):
    def setUp(self):
        self.evento = Evento(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
            data_inicio=timezone.now(),  # '2014-03-21 17:59:00',
            data_fim=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.evento.save()

        arquivo = FileFiler()
        arquivo.save()

        self.anexo = AnexoEvento(
            evento=self.evento,
            descricao=u'foto1',
            arquivo=arquivo,
        )

    def test_criacao(self):
        """
        Anexo deve possuir descricao e arquivo
        """
        self.anexo.save()
        self.assertIsNotNone(self.anexo.pk)

    def test_unicode(self):
        """
        Anexo deve apresentar descricao como unicode
        """
        self.assertEqual(u'foto1', unicode(self.anexo))


class VideoTest(TestCase):
    def setUp(self):
        self.obj = Video(
            campus_origem='RTR',
            titulo=u'Título',
            slug='titulo',
            texto=u'seu texto aqui!!!',
            video=u'ID_do_video',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )

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
        self.assertEqual(reverse('conteudo:video_detalhe', kwargs={'video_id': self.obj.id}),
                         self.obj.get_absolute_url())


class GaleriaTest(TestCase):
    def setUp(self):
        self.obj = Galeria(
            campus_origem='RTR',
            titulo=u'Título',
            slug='titulo',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )

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
        self.assertEqual(reverse('conteudo:galeria_detalhe', kwargs={'galeria_id': self.obj.id}),
                         self.obj.get_absolute_url())


class ImagemGaleriaTest(TestCase):
    def setUp(self):
        self.galeria = Galeria(
            campus_origem='RTR',
            titulo=u'Título',
            slug='titulo',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.galeria.save()

        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        self.anexo = ImagemGaleria(
            galeria=self.galeria,
            descricao=u'foto1',
            imagem=midia_image,
        )

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
