# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core.files import File
from django.contrib.auth.models import User
from filer.models import Image
from model_mommy import mommy


def preparar():
    adminuser = User.objects.create_user('admin', 'admin@test.com', 'admin')
    adminuser.save()
    adminuser.is_superuser = True
    adminuser.is_staff = True
    adminuser.save()

    site = mommy.make('Site', domain='rtr.ifmt.edu.br', name='Portal IFMT - RTR')
    site2 = mommy.make('Site', domain='cnp.ifmt.edu.br', name='Portal IFMT - CNP')
    site3 = mommy.make('Site', domain='cba.ifmt.edu.br', name='Portal IFMT - CBA')

    # cria a permissao para o usuario
    permissao = mommy.make('Permissao', user=adminuser)

    # adiciona os sites a permissao do usuario
    permissao.sites.add(site)
    permissao.sites.add(site2)

    campus = mommy.make('Campus')

    contexto = dict()
    contexto['adminuser'] = adminuser
    contexto['site'] = site
    contexto['site2'] = site2
    contexto['site3'] = site3
    contexto['permissao'] = permissao
    contexto['campus'] = campus

    return contexto


class NoticiaAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            n = mommy.make('Noticia', titulo=u'titulonoticia%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site)
            n.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            n = mommy.make('Noticia', titulo=u'titulonoticia%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            n = mommy.make('Noticia', titulo=u'titulonoticia%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3
            n.sites.add(self.site2)
            n.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_noticias_permitidas(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:conteudo_noticia_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'titulonoticia', 6)


class EventoAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            n = mommy.make('Evento', titulo=u'tituloevento%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site)
            n.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            n = mommy.make('Evento', titulo=u'tituloevento%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            n = mommy.make('Evento', titulo=u'tituloevento%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3
            n.sites.add(self.site2)
            n.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_eventos_permitidos(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:conteudo_evento_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'tituloevento', 6)


class PaginaAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            n = mommy.make('Pagina', titulo=u'titulopagina%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site)
            n.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            n = mommy.make('Pagina', titulo=u'titulopagina%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            n = mommy.make('Pagina', titulo=u'titulopagina%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3
            n.sites.add(self.site2)
            n.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_paginas_permitidas(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:conteudo_pagina_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'titulopagina', 6)


class VideoAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            n = mommy.make('Video', titulo=u'titulovideo%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site)
            n.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            n = mommy.make('Video', titulo=u'titulovideo%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            n = mommy.make('Video', titulo=u'titulovideo%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3
            n.sites.add(self.site2)
            n.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_videos_permitidos(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:conteudo_video_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'titulovideo', 6)


class GaleriaAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            n = mommy.make('Galeria', titulo=u'titulogaleria%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site)
            n.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            n = mommy.make('Galeria', titulo=u'titulogaleria%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            n = mommy.make('Galeria', titulo=u'titulogaleria%d' % i, slug=u'slug%d' % i, campus_origem=self.campus)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3
            n.sites.add(self.site2)
            n.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_galerias_permitidas(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:conteudo_galeria_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'titulogaleria', 6)


class LicitacaoAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            n = mommy.make('Licitacao', titulo=u'titulolicitacao%d' % i)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site)
            n.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            n = mommy.make('Licitacao', titulo=u'titulolicitacao%d' % i)
            # o usuario deve conseguir visualizar estas noticias
            n.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            n = mommy.make('Licitacao', titulo=u'titulolicitacao%d' % i)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3
            n.sites.add(self.site2)
            n.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_licitacoes_permitidas(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:conteudo_licitacao_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'titulolicitacao', 6)


class BannerAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']

        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagembanner'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            self.midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            banner = mommy.make('Banner', titulo=u'BannerTesteTitulo%d' % i, arquivo=self.midia_image)
            # o usuario deve conseguir visualizar estes banners
            banner.sites.add(self.site)
            banner.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            banner = mommy.make('Banner', titulo=u'BannerTesteTitulo%d' % i, arquivo=self.midia_image)
            # o usuario deve conseguir visualizar estes banners
            banner.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            banner = mommy.make('Banner', titulo=u'BannerTesteTitulo%d' % i, arquivo=self.midia_image)
            # o usuario nao deve conseguir visualizar estes banners pois nao tem permissao para o self.site3
            banner.sites.add(self.site2)
            banner.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_banners_permitidos(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:banner_banner_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'BannerTesteTitulo', 6)


class BannerARAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']

        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagembanner'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            self.midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            banner = mommy.make('BannerAcessoRapido', titulo=u'BannerTesteTitulo%d' % i, midia_image=self.midia_image)
            # o usuario deve conseguir visualizar estes banners
            banner.sites.add(self.site)
            banner.sites.add(self.site2)

        for i in range(2, 6):  # loop 4x
            banner = mommy.make('BannerAcessoRapido', titulo=u'BannerTesteTitulo%d' % i, midia_image=self.midia_image)
            # o usuario deve conseguir visualizar estes banners
            banner.sites.add(self.site2)

        for i in range(7, 12):  # loop 5x
            banner = mommy.make('BannerAcessoRapido', titulo=u'BannerTesteTitulo%d' % i, midia_image=self.midia_image)
            # o usuario nao deve conseguir visualizar estes banners pois nao tem permissao para o self.site3
            banner.sites.add(self.site2)
            banner.sites.add(self.site3)

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_banners_permitidos(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:banner_banneracessorapido_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'BannerTesteTitulo', 6)


class MenuAdminIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

        for i in range(0, 2):  # loop 2x
            mommy.make('Menu', titulo=u'titulomenu%d' % i, slug=u'slug%d' % i, site=self.site)
            # o usuario deve conseguir visualizar estas noticias

        for i in range(2, 6):  # loop 4x
            mommy.make('Menu', titulo=u'titulomenu%d' % i, slug=u'slug%d' % i, site=self.site2)
            # o usuario deve conseguir visualizar estas noticias

        for i in range(7, 12):  # loop 5x
            mommy.make('Menu', titulo=u'titulomenu%d' % i, slug=u'slug%d' % i, site=self.site3)
            # o usuario nao deve conseguir visualizar estas noticias pois nao tem permissao para o self.site3

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_licitacoes_permitidas(self):
        """
        O usuario so podera ver as noticias que estiverem publicadas nos sites no qual ele tem permissao. Ex.:
        1 - Uma noticia e publicada no site RTR e CNP
            1.1 - Caso o usuario tenha permissao para publicacao nos sites RTR e CNP:
                1.1.1 - O usuario pode visualizar essa noticia na listagem de noticias
            1.2 - Caso o usuario tenha permissao para publicacao somente no site RTR:
                1.2.1 - O usuario nao pode visualizar a noticias na listagem de noticias
        Isto e, somente se o usuario possuir permissao para todos os sites onde a noticia foi publicada ele pode
        visualiza-la na listagem
        """
        response = self.client.get(reverse('admin:core_menu_changelist'))

        # neste caso somente os 6 titulos referentes ao self.site e self.site2 (primeiro e segundo for loop do setUp)
        # devem aparecer para o usuario
        self.assertContains(response, 'titulomenu', 6)


class AddViewSitesTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']

        self.client.login(username='admin', password='admin')

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_noticias_permitidas(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:conteudo_noticia_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_paginas_permitidas(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:conteudo_pagina_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_eventos_permitidos(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:conteudo_evento_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_videos_permitidos(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:conteudo_video_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_galerias_permitidas(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:conteudo_galeria_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_licitacoes_permitidas(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:conteudo_licitacao_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_menus_permitidos(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:core_menu_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_banners_permitidas(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:banner_banner_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_bannersacessorapido_permitidas(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        response = self.client.get(reverse('admin:banner_banneracessorapido_add'))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)


class ChangeViewSitesTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    def setUp(self):

        contexto = preparar()
        self.site = contexto['site']
        self.site2 = contexto['site2']
        self.site3 = contexto['site3']
        self.campus = contexto['campus']

        self.client.login(username='admin', password='admin')

    def tearDown(self):
        self.client.logout()

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_noticia(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Noticia', titulo=u'titulonoticia', slug=u'slug', campus_origem=self.campus)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:conteudo_noticia_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_pagina(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Pagina', titulo=u'titulopagina', slug=u'slug', campus_origem=self.campus)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:conteudo_pagina_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_evento(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Evento', titulo=u'tituloevento', slug=u'slug', campus_origem=self.campus)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:conteudo_evento_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_video(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Video', titulo=u'titulovideo', slug=u'slug', campus_origem=self.campus)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:conteudo_video_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_galeria(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Galeria', titulo=u'titulogaleria', slug=u'slug', campus_origem=self.campus)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:conteudo_galeria_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_licitacao(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Licitacao', titulo=u'titulolicitacao')
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:conteudo_licitacao_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_menu(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        self.obj = mommy.make('Menu', titulo=u'titulomenu', slug=u'slug', site=self.site)

        response = self.client.get(reverse('admin:core_menu_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_banner(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagembanner'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            self.midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

        self.obj = mommy.make('Banner', titulo=u'titulobanner', arquivo=self.midia_image)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:banner_banner_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def test_sites_banneracessorapido(self):
        """
        Na admin add view deve estar disponivel somente os sites que o usuario tem permissao
        """
        img_path = 'portal/banner/static/img/images.jpeg'
        img_name = 'imagembanner'
        with open(img_path) as img:
            file_obj = File(img, name=img_name)
            self.midia_image = Image.objects.create(original_filename=img_name, file=file_obj)

        self.obj = mommy.make('BannerAcessoRapido', titulo=u'titulobanneracessorapido', midia_image=self.midia_image)
        self.obj.sites.add(self.site)

        response = self.client.get(reverse('admin:banner_banneracessorapido_change', args=(self.obj.id,)))

        # o usuario tem permissao somente para os self.site e self.site2
        # (devendo aparecer o dominio desses sites 1 vez cada)
        self.assertContains(response, self.site.domain, 1)
        self.assertContains(response, self.site2.domain, 1)
        self.assertContains(response, self.site3.domain, 0)

