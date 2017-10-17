from django.test import TestCase
from django.core.urlresolvers import resolve

from reports.views import report_cement_index


class ReportURLTestCase(TestCase):

    def test_root_url_uses_unload_list_view(self):
        """
        Отчет по цементу обрабатывается правильной функцией
        """
        root = resolve('/report/cement/')
        self.assertEqual(root.func, report_cement_index)
