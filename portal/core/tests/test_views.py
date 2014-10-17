# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.contrib.sites.models import Site
from django.utils import timezone
from model_mommy import mommy
from filer.models import Image

from portal.conteudo.models import Noticia
from portal.conteudo.models import Evento
from portal.banner.models import Banner
from portal.core.models import Menu
from portal.core.models import Destino
from portal.core.models import Selecao, TipoSelecao, Campus


class HomeTest(TestCase):
    def setUp(self):
        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
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


class HomePortalContextTest(TestCase):
    def setUp(self):
        campus = mommy.make(Campus)
        mommy.make(Noticia, _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')
        mommy.make(Noticia, _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=5, campus_origem=campus, titulo=u'test1')
        mommy.make(Evento, _quantity=3, campus_origem=campus, titulo=u'Titulo do evento')

        self.site = mommy.make(Site, _quantity=1, domain='rtr.ifmt.dev')[0]

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
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


class HomeBlogContextTest(TestCase):
    def setUp(self):
        campus = mommy.make(Campus)
        mommy.make(
            'Noticia', _quantity=8, campus_origem=campus, titulo=u'test1', destaque=True,
            publicado=True, data_publicacao=timezone.now())
        mommy.make(
            'Noticia', _quantity=9, campus_origem=campus, titulo=u'test1',
            publicado=True, data_publicacao=timezone.now())

        self.site = mommy.make(Site, domain='rtr.ifmt.dev')

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.blog(), caminho='core/blog.html')
        sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in Noticia.objects.all():
            i.sites.add(self.site)

        for i in Evento.objects.all():
            i.sites.add(self.site)

        # cria o ambiente de um novo site e conteudos para simular ambiente real
        self.site2 = mommy.make(Site, domain='cba.ifmt.dev')
        noticias_destaque = mommy.make(Noticia, _quantity=4, campus_origem=campus,
                                       titulo=u'noticia_destaque', destaque=True)
        noticias = mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')

        for i in noticias_destaque:
            i.sites.add(self.site2)
        for i in noticias:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET / deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Pagina detalhe deve renderizar o template portal_secundario.html
        """
        self.assertTemplateUsed(self.resp, 'core/blog.html')

    def test_conteudo_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque
        """
        # Sao esperados 5 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'test1', 5)


class HomeBlogSliderContextTest(TestCase):
    def setUp(self):
        campus = mommy.make(Campus)
        mommy.make(Noticia, _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')
        mommy.make(Noticia, _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make(Noticia, _quantity=5, campus_origem=campus, titulo=u'test1')

        self.site = mommy.make(Site, domain='rtr.ifmt.dev')

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.blog_slider(), caminho='core/blog_slider.html')
        sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in Noticia.objects.all():
            i.sites.add(self.site)

        # cria o ambiente de um novo site e conteudos para simular ambiente real
        self.site2 = mommy.make(Site, domain='cba.ifmt.dev')
        noticias_destaque = mommy.make(Noticia, _quantity=4, campus_origem=campus,
                                       titulo=u'noticia_destaque', destaque=True)
        noticias = mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')

        for i in noticias_destaque:
            i.sites.add(self.site2)
        for i in noticias:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET / deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Pagina detalhe deve renderizar o template portal_secundario.html
        """
        self.assertTemplateUsed(self.resp, 'core/blog_slider.html')

    def test_conteudo_mais_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque+
        """
        # Sao esperados 9 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'test1', 5)

    def test_conteudo_noticias_destaque(self):
        """
        A home de conter noticias de destaque no topo e pode tambem existir na listagem
        """
        # Sao esperados 5 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        # Como sao exibidos os thumbnails para navegacao esse numero duplica, ficando 10
        self.assertContains(self.resp, u'noticia_destaque', 5)


class HomePortalSecundarioContextTest(TestCase):
    def setUp(self):
        campus = mommy.make(Campus)
        mommy.make('Noticia', _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make('Noticia', _quantity=7, campus_origem=campus, titulo=u'test1')
        mommy.make('Noticia', _quantity=4, campus_origem=campus, titulo=u'noticia_destaque', destaque=True)
        mommy.make('Noticia', _quantity=5, campus_origem=campus, titulo=u'test1')
        mommy.make('Evento', _quantity=3, campus_origem=campus, titulo=u'Titulo do evento')

        self.site = mommy.make(Site, domain='rtr.ifmt.dev')

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.portal_secundario(), caminho='core/portal_secundario.html')
        sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner destaque', arquivo=midia_image, tipo=1)
        mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner link de acesso', arquivo=midia_image, tipo=2)

        sitedetalhe.site = self.site
        sitedetalhe.save()

        for i in Noticia.objects.all():
            i.sites.add(self.site)

        for i in Evento.objects.all():
            i.sites.add(self.site)

        for i in Banner.objects.all():
            i.sites.add(self.site)

        # cria o ambiente de um novo site e conteudos para simular ambiente real
        self.site2 = mommy.make(Site, domain='cba.ifmt.dev')
        noticias_destaque = mommy.make(Noticia, _quantity=4, campus_origem=campus,
                                       titulo=u'noticia_destaque', destaque=True)
        noticias = mommy.make(Noticia, _quantity=7, campus_origem=campus, titulo=u'test1')
        eventos = mommy.make(Evento, _quantity=3, campus_origem=campus, titulo=u'Titulo do evento')
        banners = mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner destaque', arquivo=midia_image, tipo=1)
        banners_link = mommy.make('Banner', _quantity=5, titulo=u'Titulo do banner link de acesso',
                                  arquivo=midia_image, tipo=2)

        for i in noticias_destaque:
            i.sites.add(self.site2)
        for i in noticias:
            i.sites.add(self.site2)
        for i in eventos:
            i.sites.add(self.site2)
        for i in banners:
            i.sites.add(self.site2)
        for i in banners_link:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET / deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Pagina detalhe deve renderizar o template portal_secundario.html
        """
        self.assertTemplateUsed(self.resp, 'core/portal_secundario.html')

    def test_conteudo_mais_noticias(self):
        """
        A home deve conter noticias listadas na parte nao destaque+
        """
        # Sao esperados 6 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'test1', 6)

    def test_conteudo_evento(self):
        """
        A home deve conter tres eventos
        """
        self.assertContains(self.resp, u'Titulo do evento', 3)

    def test_banners_destaque(self):
        """
        A home deve conter 4 banners (duplicado devido ao tooltip)
        """
        self.assertContains(self.resp, u'Titulo do banner destaque', 8)

    def test_banners_linkdeacesso(self):
        """
        A home deve conter 5 banners (duplicado devido ao tooltip)
        """
        self.assertContains(self.resp, u'Titulo do banner link de acesso', 10)

    def test_conteudo_noticias_destaque(self):
        """
        A home de conter noticias de destaque no topo e pode tambem existir na listagem
        """
        # Sao esperados 5 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        # Como sao exibidos os thumbnails para navegacao esse numero duplica, ficando 10
        self.assertContains(self.resp, u'noticia_destaque', 10)


class HomeBannersContextTest(TestCase):
    def setUp(self):
        self.site = mommy.make(Site, domain='rtr.ifmt.dev')

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.banners(), caminho='core/banners.html')
        mommy.make('SiteDetalhe', destino=destino, logo=midia_image, site=self.site)

        mommy.make('Banner', _quantity=4, titulo=u'banner', arquivo=midia_image)

        for i in Banner.objects.all():
            i.sites.add(self.site)

        # cria o ambiente de um novo site e conteudos para simular ambiente real
        self.site2 = mommy.make('Site', domain='cba.ifmt.dev')
        outros_banners = mommy.make('Banner', _quantity=4, titulo=u'banner', arquivo=midia_image)

        for i in outros_banners:
            i.sites.add(self.site2)

        self.resp = self.client.get(reverse('home'), SERVER_NAME='rtr.ifmt.dev')

    def test_get(self):
        """
        GET / deve retorno status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Pagina detalhe deve renderizar o template portal_secundario.html
        """
        self.assertTemplateUsed(self.resp, 'core/banners.html')

    def test_banners(self):
        """
        A home deve conter noticias listadas na parte nao destaque+
        """
        # Sao esperados 4 noticias desse tipo pois no setup foi simulado uma ordem aleatoria
        self.assertContains(self.resp, u'banner', 8)


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

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
        with open(self.img_path) as img:
            file_obj = File(img, name=self.img_name)
            midia_image = Image.objects.create(original_filename=self.img_name, file=file_obj)

        destino = mommy.make('Destino', tipo=Destino.portal(), caminho='core/portal.html')
        self.sitedetalhe = mommy.make('SiteDetalhe', destino=destino, logo=midia_image)

        self.site.sitedetalhe = self.sitedetalhe
        self.site.sitedetalhe.save()

        for i in range(0, 7):
            self.menu = Menu(
                parent=None,
                titulo=u'TituloMenu',
                url=u'url_menu',
                ordem=1,
                site=self.site,
            )
            self.menu.save()

        # cria um novo site e menus pertencentes a este novo site para simular ambiente real
        self.site2 = mommy.make(Site, _quantity=1, domain='cba.ifmt.dev')[0]
        for i in range(10, 17):
            self.menu2 = Menu(
                parent=None,
                titulo=u'TituloMenu',
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
        campus = mommy.make('Campus')

        self.site = mommy.make('Site', domain='rtr.ifmt.dev')

        self.img_path = u'portal/banner/static/img/images.jpeg'
        self.img_name = u'imagembanner'
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
        self.site2 = mommy.make(Site, domain='cba.ifmt.dev')
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