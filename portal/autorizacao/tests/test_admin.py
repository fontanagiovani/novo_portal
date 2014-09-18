# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from django.test.utils import override_settings


def preparar():
    adminuser = User.objects.create_user('admin', 'admin@test.com', 'admin')
    adminuser.save()
    adminuser.is_superuser = True
    adminuser.is_staff = True
    adminuser.save()

    site = mommy.make('Site', domain='ifmt.edu.br', name='Portal IFMT')
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

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
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
    def test_usuario_pode_ver_somente_noticias_permitidas(self):
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

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
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
    def test_usuario_pode_ver_somente_eventos_permitidos(self):
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
