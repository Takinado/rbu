import time

from django.core.urlresolvers import resolve
from django.test import TestCase, RequestFactory
from django.test import LiveServerTestCase

from selenium import webdriver


from .views import report_index


class IndexTestCase(LiveServerTestCase):

    def setUp(self):
        # driver = webdriver.Firefox()
        # time.sleep(5)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_last_status(self):
        """
        Test that a user can search for solos
        """
        home_page = self.browser.get(self.live_server_url + '/')
        # of the site in the heading.
        brand_element = self.browser.find_element_by_css_selector('h2#last-status')
        self.assertNotEqual('Последний статус None', brand_element.text)
        # self.fail('Incomplete Test')

    def tearDown(self):
        pass
        self.browser.quit()


class StatusURLsTestCase(TestCase):

    def test_root_url_uses_index_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, report_index)


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/')
        with self.assertTemplateUsed('report/index.html'):
            response = report_index(request)
            self.assertEqual(response.status_code, 200)

