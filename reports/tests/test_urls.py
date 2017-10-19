from datetime import datetime

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve

from reports.views import report_cement_index, CementMonthArchiveView


class ReportURLTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_root_url_uses_cement_report_view(self):
        """
        Отчет по цементу обрабатывается правильной функцией
        """
        root = resolve('/report/cement/')
        self.assertEqual(root.func, report_cement_index)
