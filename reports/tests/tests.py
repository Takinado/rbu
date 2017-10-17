from datetime import datetime, date

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from reports.models import Cement


class ReportTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        cement1 = Cement.objects.create_cement(date.today(), 100)

    def find_search_results(self):
        return self.browser.find_elements_by_css_selector('.cement-li')

    def test_view_report(self):
        """
        Тест что пользователь может просматривать статусы
        :return:
        """

        home_page = self.browser.get(self.live_server_url + '/report/cement/')

        try:
            brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        except NoSuchElementException:
            return self.fail('Не открывается страница Отчёта цемента. На странице не найден элемент ".navbar-brand"')

        self.assertEqual('РБУ', brand_element.text)

        # На странице список Цементов за текущий месяц
        search_results = self.find_search_results()
        self.assertGreaterEqual(len(search_results), 1)

        # # Можно выбрать дату и отправить запрос
        # date_input.send_keys('07.08.2017')
        # self.browser.find_element_by_css_selector('form button').click()
        #
        # # И увидеть результат... статусы за дату
        # search_results = self.find_search_results()
        # self.assertEqual(len(search_results), 2)
        #
        # # Можно выбрать статус
        # search_results[0].click()
        #
        # # На странице отгрузки увидеть дату, время и все данные из модели
        # # Числом статусов: общим, с ошибками, с предупреждениями, не посчитаных, без отгрузки
        # # а также модель фото и если нужно фото
        # # ссылку на отгрузку
        # date_url = datetime.strftime(datetime.now(), "%Y/%m/%d")
        #
        # self.assertEqual(
        #     self.browser.current_url,
        #     '{}/status/3/'.format(self.live_server_url)
        # )
        #
        # try:
        #     brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        # except NoSuchElementException:
        #     return self.fail('Не открывается страница Статуса. На странице не найден элемент ".navbar-brand"')
        #
        # self.assertEqual(
        #     self.browser.find_element_by_css_selector('#status-date').text,
        #     '07.08.2017'
        # )

        self.fail('Весь тест пока не выполняется')

    def tearDown(self):
        self.browser.quit()
        pass
