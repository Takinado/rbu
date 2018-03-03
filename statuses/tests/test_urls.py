from django.core.urlresolvers import resolve
from django.test import TestCase

from statuses.views import index_statuses_view, StatusDayView, StatusDetailView


class StatusURLTestCase(TestCase):

    def test_root_url_uses_unload_list_view(self):
        """
        Тест что status_list_view обрабатывается правильной функцией
        """
        # brand_element = self.browser.find_element_by_css_selector('#unload-list-link')
        root = resolve('/status/')
        self.assertEqual(root.func, index_statuses_view)

    def test_url_uses_unload_list_view(self):
        """
        Тест что status_list_view c датой обрабатывается правильной функцией
        """
        found = resolve('/status/2017/01/21/')
        self.assertEquals(found.func.__name__, StatusDayView.__name__)
        self.assertEquals(found.func.view_class, StatusDayView)

    def test_status_details_url(self):
        """
        Тест что URL от StatusDetail обрабатывается правильной функцией
        :return:
        """
        status_detail = resolve('/status/3/')

        self.assertEquals(status_detail.func.__name__, StatusDetailView.__name__)
        self.assertEquals(status_detail.func.view_class, StatusDetailView)
        self.assertEqual(status_detail.kwargs['pk'], '3')
