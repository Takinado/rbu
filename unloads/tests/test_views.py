from django.test import TestCase, RequestFactory

from statuses.views import report_index, statuses


class UnloadViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/')
        with self.assertTemplateUsed('reports/index.html'):
            response = report_index(request)
            self.assertEqual(response.status_code, 200)


# class StatusViewTestCase(TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_statuses_view_basic(self):
#         """
#         Test that statuses view returns a 200 response and uses
#         the correct template
#         """
#         request = self.factory.get('/statuses/')
#         with self.assertTemplateUsed('statuses/statuses.html'):
#             response = statuses(request)
#             self.assertEqual(response.status_code, 200)
