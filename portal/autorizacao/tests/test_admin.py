# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from django.test.utils import override_settings


class NoticiaIndexTest(TestCase):
    # Templates
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    # Remove o context processor que carrega os menus pois nao e importante para o teste
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS)
    def setUp(self):
        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'admin')
        self.adminuser.save()
        self.adminuser.is_superuser = True
        self.adminuser.is_staff = True
        self.adminuser.save()
        self.client.login(username='admin', password='admin')

        self.site = mommy.make('Site', domain='ifmt.edu.br', name='Portal IFMT')
        self.site2 = mommy.make('Site', domain='cnp.ifmt.edu.br', name='Portal IFMT - CNP')
        self.site3 = mommy.make('Site', domain='cba.ifmt.edu.br', name='Portal IFMT - CBA')

        # cria a permissao para o usuario
        self.permissao = mommy.make('Permissao', user=self.adminuser)

        # adiciona os sites a permissao do usuario
        self.permissao.sites.add(self.site)
        self.permissao.sites.add(self.site2)

        self.campus = mommy.make('Campus')

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
