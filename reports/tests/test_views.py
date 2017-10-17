# -*- coding: utf-8 -*-
from datetime import datetime

from django.test import TestCase, RequestFactory
from reports.views import report_cement_index, CementMonthArchiveView


class CementViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_cement_view_basic(self):
        """
        Test that cement_report_form view returns a 302 response
        """
        request = self.factory.get('/report/cement/')
        response = report_cement_index(request)
        self.assertEqual(response.status_code, 302)

    def test_cement_list_view_from_index_basic(self):
        """
        Тест что представление при перенаправлении с главной страницы статусов возвращает 200
        и использует правильный шаблон
        """
        year = str(datetime.now().year)
        month = str(datetime.now().month)

        request = self.factory.get('/report/cement/{}/{}/'.format(year, month))
        response = CementMonthArchiveView.as_view(month_format='%m')(request, year=year, month=month)

        with self.assertTemplateUsed('reports/cement_archive_month.html'):
            response.render()

        response2 = CementMonthArchiveView.as_view(month_format='%m')(request, year=year, month=month)
        self.assertEqual(response2.status_code, 200)

        response3 = CementMonthArchiveView.as_view(month_format='%m')(request, year=year, month=month)
        with self.assertTemplateUsed('reports/cement_archive_month.html'):
            response3.render()
            self.assertEqual(response3.status_code, 200)
