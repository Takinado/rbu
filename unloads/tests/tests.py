import datetime

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from unloads.models import Unload


class UnloadsTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        self.unload1 = Unload.objects.create(
            date=datetime.date(2017, 9, 1),
            him=4,
            cement=400,
        )
        self.unload2 = Unload.objects.create(
            date=datetime.datetime.now().date(),
            water=150,
            cement=200,
        )

        self.unload3 = Unload.objects.create(
            date=datetime.date(2017, 9, 1),
            him=4,
            water=150,
            cement=300,
        )

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

        # и общим списком отгрузок за сегодня
        search_results = self.browser.find_elements_by_css_selector('.unload-row')
        # self.assertGreater(len(search_results), 1)
        self.assertEqual(len(search_results), 1)


        # Можно выбрать дату и отправить запрос
        date_input.send_keys('01.09.2017')
        # date_input.submit()
        self.browser.find_element_by_css_selector('form button').click()

        # И увидеть результат... отгрузки за дату
        search_results = self.browser.find_elements_by_css_selector('.unload-row')
        self.assertGreater(len(search_results), 1)

        # Можно выбрать отгрузку

        # Страница отгрузки

        self.fail('Весь тест пока не выполняется')

    def tearDown(self):
        self.browser.quit()
        pass
