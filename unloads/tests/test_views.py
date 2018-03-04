# import datetime
#
# from django.db.models import QuerySet
# from django.test import TestCase, RequestFactory
#
# from unloads.models import Unload
# from unloads.views import unload_list_view, UnloadDetailView
#
#
# class UnloadBaseTestCase(TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#
#         cls.unload1 = Unload.objects.create(
#             date=datetime.date(2017, 9, 1),
#             him=4.0,
#             water=100,
#             cement=400,
#             breakstone=1280,
#             sand=700,
#             is_active_left_bunker=True,
#         )
#
#         cls.unload2 = Unload.objects.create(
#             date=datetime.datetime.strptime('02.09.2017', '%d.%m.%Y').date(),
#             him=3,
#             water=150.0,
#             cement=200.0,
#             breakstone=1000,
#             sand=500,
#             is_active_left_bunker=False,
#         )
#
#         cls.unload3 = Unload.objects.create(
#             date=datetime.date(2017, 9, 1),
#             him=0,
#             water=80,
#             is_active_left_bunker=True,
#         )
#
#
# class IndexUnloadViewTestCase(UnloadBaseTestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_unload_view_basic(self):
#         """
#         Test that view returns a 200 response and uses
#         the correct template
#         """
#         request = self.factory.get('/unload/')
#         response = unload_list_view(request)
#         with self.assertTemplateUsed('unloads/unloads_list_view.html'):
#             response = unload_list_view(request)
#             self.assertEqual(response.status_code, 200)
#
#     def test_index_unload_view_returns_unloads(self):
#         """
#         Test that the view will attempt to return
#         Unloads if query parameters exist
#         """
#         test_date = '01.09.2017'
#         response = self.client.get(
#             "/unload/",
#             {'date': test_date}
#         )
#
#         unloads = response.context['unloads']
#
#         self.assertIs(type(unloads), QuerySet)
#         self.assertGreaterEqual(len(unloads), 1)
#         self.assertEqual(unloads[0].him, 4)
#
#
# class UnloadViewTestCase(UnloadBaseTestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_basic(self):
#         """
#         Тестирование того что unload_view возращает 200,
#         использует правильный шаблон и правильный контекст
#         :return:
#         """
#         request = self.factory.get('/unload/1/')
#
#         response = UnloadDetailView.as_view()(
#             request,
#             pk=self.unload1.pk
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.context_data['unload'].date, datetime.date(2017, 9, 1)
#         )
#         with self.assertTemplateUsed('unloads/unload_detail.html'):
#             response.render()
