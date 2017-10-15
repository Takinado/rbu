# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from reports.views import cement_report_form


class CementViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_cement_view_basic(self):
        """
        Test that cement_report_form view returns a 200 response
        """
        request = self.factory.get('/report/cement/')
        response = cement_report_form(request)
        self.assertEqual(response.status_code, 200)

    def test_cement_view_basic_template(self):
        """
        Test that cement_report_form view uses the correct template
        """
        request = self.factory.get('/report/cement/')
        with self.assertTemplateUsed('reports/cement.html'):
            response = cement_report_form(request)
            self.assertEqual(response.status_code, 200)
