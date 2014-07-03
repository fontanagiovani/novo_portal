# #coding: utf-8

# from django.test import TestCase
# from portal.banner.models import Banner
# from django.core.urlresolvers import reverse
# from model_mommy import mommy
#
#É necessario pesquisar suporte do mommy ao Jango.Filer
# class HomeBannerContextTest(TestCase):
#     def setUp(self):
#         self.banner = mommy.make(Banner, _quantity=3, titulo=u'Titulo do banner')
#         self.resp = self.client.get(reverse('home'))
#
#     def test_banner(self):
#         """
#          A Home deve conter três banners
#         """
#         self.assertContains(self.resp, u'Titulo do banner', 3)
#
#
#
