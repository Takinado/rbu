from django.test import TestCase
from django.core.urlresolvers import resolve
from statuses.views import report_index, statuses


class IndexURLsTestCase(TestCase):
    def test_root_url_uses_status_list_view(self):
        """
        Test that the ... of the site resolves to the
        correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, report_index)


# class StatusURLsTestCase(TestCase):
#     def test_root_url_uses_statuses_view(self):
#         """
#         Test that the ... of the site resolves to the
#         correct view function
#         """
#         root = resolve('/statuses/')
#         self.assertEqual(root.func, statuses)
