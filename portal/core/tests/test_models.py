# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from portal.core.models import Conteudo
from portal.core.models import Midia
from filer.models import File as FileFiler
from model_mommy import mommy
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import StringIO


class ConteudoTest(TestCase):
    def setUp(self):
        self.obj = Conteudo(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )

    def test_criacao(self):
        """
        conteudo deve conter titulo, texto, data_publicacao
        """
        self.obj.save()
        self.assertIsNotNone(self.obj.pk)

    def test_unicode(self):
        """
        Conteudo deve apresentar o titulo como unicode
        """
        self.assertEqual(u'Título', unicode(self.obj))

# class ConteudoMidiaTeste(TestCase):
#     def setUp(self):
#         self.conteudo = mommy.make(Conteudo, )
#
#         io = StringIO.StringIO()
#         io.write('foo')
#         text_file = InMemoryUploadedFile(io, None, 'foo.txt', 'text', io.len, None)
#         text_file.seek(0)
#         arquivo = FileFiler(file=text_file)
#         arquivo.save()
#         self.midia_texto = Midia(
#             conteudo=self.conteudo,
#             descricao=u'foto1',
#             arquivo=arquivo
#         )
#         self.midia_texto.save()
#
#         size = (200,200)
#         color = (255,0,0,0)
#         image = Image.new("RGBA", size, color)
#         image.save(io, format='JPEG')
#         image_file = InMemoryUploadedFile(io, None, 'foo.jpg', 'jpeg', io.len, None)
#         image_file.seek(0)
#         arquivo = FileFiler(file=image_file)
#         arquivo.save()
#         self.midia_imagem = Midia(
#             conteudo=self.conteudo,
#             descricao=u'foto1',
#             arquivo=arquivo
#         )
#         self.midia_imagem.save()
#         self.conteudo.save()

    def test_primeira_imagem(self):
        """
        Deve retornar a primeira imagem de um conteudo
        """
        imagem = self.conteudo.primeira_imagem()
        self.assertEqual(self.midia_imagem.arquivo, imagem)



class MidiaTest(TestCase):
    def setUp(self):
        self.conteudo = Conteudo(
            titulo=u'Título',
            texto=u'seu texto aqui!!!',
            data_publicacao=timezone.now(),  # '2014-03-21 17:59:00',
        )
        self.conteudo.save()

        arquivo = FileFiler()
        arquivo.save()

        self.midia = Midia(
            conteudo=self.conteudo,
            descricao=u'foto1',
            arquivo=arquivo
        )

    def test_criacao(self):
        '''
        Midia deve possuir conteudo, descricao e arquivo
        '''
        self.midia.save()
        self.assertIsNotNone(self.midia.pk)


    def test_unicode(self):
        '''
        Midia deve apresentar descricao como unicode
        '''
        self.assertEqual(u'foto1', unicode(self.midia))

