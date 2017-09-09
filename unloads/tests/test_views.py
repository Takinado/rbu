from django.db.models import QuerySet
from django.test import TestCase, RequestFactory

from unloads.views import unload_list_view


class UnloadViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_unload_view_basic(self):
        """
        Test that view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/unload/')
        with self.assertTemplateUsed('unloads/unloads_list_view.html'):
            response = unload_list_view(request)
            self.assertEqual(response.status_code, 200)

    def test_unload_view_returns_unloads(self):
        """
        Test that the view will attempt to return
        Unloads if query parameters exist
        """
        response = self.client.get(
            "/unload/",
            {'unload_date': '01.09.2017'}
        )
        self.assertIs(
            type(response.context['unloads']),
            QuerySet
        )
