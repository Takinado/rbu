import time

from django.test import LiveServerTestCase

from selenium import webdriver


from statuses.views import report_index


class IndexTestCase(LiveServerTestCase):

    def setUp(self):
        # driver = webdriver.Firefox()
        # time.sleep(5)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_index_view(self):
        """
        Test that a user can search for solos
        """
        home_page = self.browser.get(self.live_server_url + '/')
        # of the site in the heading.
        brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        self.assertEqual('РБУ', brand_element.text)
        # self.fail('Incomplete Test')

    def tearDown(self):
        pass
        self.browser.quit()


class StatusTestCase(LiveServerTestCase):

    def setUp(self):
        # driver = webdriver.Firefox()
        # time.sleep(5)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_statuses_view(self):
        """
        Test that a user can search for solos
        """
        home_page = self.browser.get(self.live_server_url + '/statuses/')
        # of the site in the heading.
        brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        self.assertEqual('РБУ', brand_element.text)

    def tearDown(self):
        pass
        self.browser.quit()
