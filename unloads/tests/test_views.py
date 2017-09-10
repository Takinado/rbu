import datetime

from django.db.models import QuerySet
from django.test import TestCase, RequestFactory

from unloads.models import Unload
from unloads.views import unload_list_view


class UnloadViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.unload1 = Unload.objects.create(
            date=datetime.date(2017, 9, 1),
            him=4,
            cement=400,
        )
        self.unload2 = Unload.objects.create(
            date=datetime.datetime.strptime('02.09.2017', '%d.%m.%Y').date(),
            water=150,
            cement=200,
        )

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
        test_date = '01.09.2017'
        response = self.client.get(
            "/unload/",
            {'date': test_date}
        )

        unloads = response.context['unloads']

        self.assertIs(type(unloads), QuerySet)
        self.assertEqual(len(unloads), 1)
        self.assertEqual(unloads[0].him, 4)
