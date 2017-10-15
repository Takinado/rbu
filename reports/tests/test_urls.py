from django.test import TestCase
from django.core.urlresolvers import resolve

from reports.views import cement_report_form


class ReportURLTestCase(TestCase):

    def test_root_url_uses_unload_list_view(self):
        """
        Отчет по цементу обрабатывается правильной функцией
        """
        root = resolve('/report/cement/')
        self.assertEqual(root.func, cement_report_form)

    #
    # def test_url_uses_unload_list_view(self):
    #     """
    #     Тест что status_list_view c датой обрабатывается правильной функцией
    #     """
    #     found = resolve('/status/2017/08/07/')
    #     self.assertEquals(found.func.__name__, StatusDayView.__name__)
    #     self.assertEquals(found.func.view_class, StatusDayView)
    #
    # def test_status_details_url(self):
    #     """
    #     Тест что URL от StatusDetail обрабатывается правильной функцией
    #     :return:
    #     """
    #     status_detail = resolve('/status/3/')
    #
    #     self.assertEquals(status_detail.func.__name__, StatusDetailView.__name__)
    #     self.assertEquals(status_detail.func.view_class, StatusDetailView)
    #     self.assertEqual(status_detail.kwargs['pk'], '3')
