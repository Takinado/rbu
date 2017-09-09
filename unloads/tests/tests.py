from django.test import LiveServerTestCase
#
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

        home_page = self.browser.get(self.live_server_url + '/unload')

        # brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        # self.assertEqual('РБУ', brand_element.text)

        try:
            brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        except NoSuchElementException:
            return self.fail('Не открывается страница Выгрузок. На странице не найден элемент ".navbar-brand"')

        self.assertEqual('РБУ', brand_element.text)

        # На странице форма с выбором даты
        date_input = self.browser.find_element_by_css_selector(
            'input#unload-date'
        )
        self.assertIsNotNone(self.browser.find_element_by_css_selector(
            'label[for="unload-date"]'))
        self.assertEqual(date_input.get_attribute('placeholder'),
                         '22.03.1981')

        # Можно выбрать дату и отправить запрос
        date_input.send_keys('01.09.2017')
        date_input.submit()

        # И увидеть результат
        search_results = self.browser.find_elements_by_css_selector('.unload-search-result')
        self.assertGreater(len(search_results), 1)

        # Второй пример со списком
        # date_input = self.browser.find_element_by_css_selector('input#unload-date')
        # date_input.send_keys('01.09.2017')
        # self.browser.find_element_by_css_selector('form button').click()
        # # second_search_results = self.search_results()
        search_results2 = self.browser.find_elements_by_css_selector('.unload-search-result')

        self.assertEqual(len(search_results2), 2)


#         # Есть ссылка на главной
#         home_page = self.browser.get(self.live_server_url + '/')
#         brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
#         self.assertEqual('РБУ', brand_element.text)
#         try:
#             brand_element = self.browser.find_element_by_css_selector('#unload-list-link')
#         except NoSuchElementException:
#             return self.assertTrue(False)
#
#         # Можно перейти на неё
#
#         print(brand_element.get_attribute('href'))
#         unloads_page = self.browser.get(brand_element.get_attribute('href'))
#         brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
#         self.assertEqual('РБУ', brand_element.text)


    # На странице форма с выбором даты

    # При выборе даты видны отгрузки за дату

    # Можно выбрать отгрузку

    # Страница отгрузки

    def tearDown(self):
        self.browser.quit()
