# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.contrib.sites.models import Site
from model_mommy import mommy
from filer.models import Image

from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.core.models import Menu
from portal.core.models import Destino, SiteDetalhe
from portal.core.models import Selecao, TipoSelecao, Campus


class HomeTest(TestCase):
    def setUp(self):
        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]

        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

        sitedetalhe.site = self.site
        sitedetalhe.save()

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET / must return status code 200.
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Home must use template core/portal.html
        """
        self.assertTemplateUsed(self.resp, 'core/portal.html')


class HomeContextTest(TestCase):
    def setUp(self):
        campus = mommy.make(Campus, _quantity=1, slug='abc')[0]
        mommy.make(Noticia, _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')
        mommy.make(Noticia, _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=5, campus_origem=campus, titulo=u'test1')
        mommy.make(Evento, _quantity=3, campus_origem=campus, titulo=u'Titulo do evento')

        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]

        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in Noticia.objects.all():
            i.sites.add(self.site)

        for i in Evento.objects.all():
            i.sites.add(self.site)

        # cria o ambiente de um novo site e conteudos para simular ambiente real
        self.site2 = mommy.make(Site, _quantity=1, domain='cba.ifmt.dev')[0]
        noticias_destaque = mommy.make(Noticia, _quantity=4, campus_origem=campus,
                                       titulo=u'noticia_destaque', destaque=True)
        noticias = mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')
        eventos = mommy.make(Evento, _quantity=3, campus_origem=campus, titulo=u'Titulo do evento')

        for i in noticias_destaque:
            i.sites.add(self.site2)
        for i in noticias:
            i.sites.add(self.site2)
        for i in eventos:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_conteudo_mais_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque+
        """
        # Sao esperados 9 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'test1', 10)

    def test_conteudo_evento(self):
        """
        A home deve conter tres eventos
        """
        self.assertContains(self.resp, u'Titulo do evento', 3)

    def test_conteudo_noticias_destaque(self):
        """
        A home de conter noticias de destaque no topo e pode tambem existir na listagem
        """
        # Sao esperados 5 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        # Como sao exibidos os thumbnails para navegacao esse numero duplica, ficando 10
        self.assertContains(self.resp, u'noticia_destaque', 10)


class SelecaoTest(TestCase):
    def setUp(self):
        self.tipo = TipoSelecao(
            parent=None,
            titulo=u'Título',
            slug='titulo'
        )
        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]

        self.tipo.save()
        self.selecao = mommy.make(Selecao, titulo='titulo_teste', tipo=self.tipo, _quantity=50)
        self.menuselecao = mommy.make(TipoSelecao, titulo=u'test1', _quantity=7)

        self.resp = self.client.get(reverse('selecao'), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET /selecao/ deve retornar status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Eventos lista deve renderizar o template selecao_lista.html
        """
        self.assertTemplateUsed(self.resp, 'core/selecao_lista.html')

    def test_menu_selecao(self):
        self.assertContains(self.resp, u'test1', 7)


class Menutest(TestCase):
    def setUp(self):
        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]
        self.template = mommy.make(Destino, _quantity=1, tipo=Destino.portal(), caminho='core/portal.html')[0]

        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        self.sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

        self.site.sitedetalhe = self.sitedetalhe
        self.site.sitedetalhe.save()

        for i in range(0, 7):
            slug = u'TituloMenu - %d' % i
            self.menu = Menu(
                parent=None,
                titulo=u'TituloMenu',
                slug=slug,
                url=u'url_menu',
                ordem=1,
                site=self.site,
            )
            self.menu.save()

        # cria um novo site e menus pertencentes a este novo site para simular ambiente real
        self.site2 = mommy.make(Site, _quantity=1, domain='cba.ifmt.dev')[0]
        for i in range(10, 17):
            slug = u'TituloMenu - %d' % i
            self.menu2 = Menu(
                parent=None,
                titulo=u'TituloMenu',
                slug=slug,
                url=u'url_menu',
                ordem=1,
                site=self.site2,
            )
            self.menu2.save()

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_context_menu(self):
        """
        A home deve conter sete menus padrão
        """
        self.assertContains(self.resp, u'TituloMenu', 7)


class DestinoTest(TestCase):
    def setUp(self):
        campus = mommy.make('Campus', slug='abc')

        self.site = mommy.make('Site', domain='rtr.ifmt.dev')

        self.img_path = 'portal/banner/static/img/images.jpeg'
        self.img_name = 'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        mommy.make('SiteDetalhe', site=self.site, destino=destino, logo=midia_image)

        for i in Noticia.objects.all():
            i.sites.add(self.site)

        for i in Evento.objects.all():
            i.sites.add(self.site)

        # cria o ambiente de um novo site e conteudos para simular ambiente real
        self.site2 = mommy.make(Site, _quantity=1, domain='cba.ifmt.dev')[0]
        noticias_destaque = mommy.make(Noticia, _quantity=4, campus_origem=campus,
                                       titulo=u'noticia_destaque', destaque=True)
        noticias = mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')
        eventos = mommy.make(Evento, _quantity=3, campus_origem=campus, titulo=u'Titulo do evento')

        for i in noticias_destaque:
            i.sites.add(self.site2)
        for i in noticias:
            i.sites.add(self.site2)
        for i in eventos:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')