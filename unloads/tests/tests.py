from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class UnloadsTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_view_unload(self):
        """
        Тест что пользователь мжет просматривать отгрузки
        :return:
        """
        # Есть ссылка на главной
        home_page = self.browser.get(self.live_server_url + '/')
        brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        self.assertEqual('РБУ', brand_element.text)
        try:
            brand_element = self.browser.find_element_by_css_selector('#unload-list-link')
        except NoSuchElementException:
            return self.assertTrue(False)

        # Можно перейти на неё

        print(brand_element.get_attribute('href'))
        unloads_page = self.browser.get(brand_element.get_attribute('href'))
        brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        self.assertEqual('РБУ', brand_element.text)

        # На странице форма с выбором даты

        # При выборе даты видны отгрузки за дату

        # Можно выбрать отгрузку

        # Страница отгрузки

        self.fail('Весь тест пока не выполняется')

    def tearDown(self):
        self.browser.quit()
