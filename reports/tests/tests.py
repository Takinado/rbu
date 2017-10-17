from datetime import datetime, date, timedelta

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from reports.models import Cement


class ReportTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        now_date = date.today()

        cement1 = Cement.objects.create_cement(now_date, 100)
        cement2 = Cement.objects.create_cement(now_date - timedelta(days=1), 200)
        cement3 = Cement.objects.create_cement(now_date.replace(month=now_date.month-1), 150)

    def find_search_results(self):
        return self.browser.find_elements_by_css_selector('.cement-li')

    def test_view_report(self):
        """
        Тест что пользователь может просматривать отчет по цементу
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
        self.assertGreaterEqual(len(search_results), 2)

        # Совпадает кол-во дней за месяц на странице и в тотал
        total_day = self.browser.find_element_by_css_selector('#total-day').text
        self.assertEqual(len(search_results), int(total_day))

        # Совпадает сумма цемента за месяц на странице и в тотал
        total_value = self.browser.find_element_by_css_selector('#total-value').text
        cement_values_tag = self.browser.find_elements_by_css_selector('.cement-value')
        cement_values = [val.text for val in cement_values_tag]
        self.assertEqual(int(total_value), sum(map(int, cement_values)))

        # есть ссылка и можно перейти на прошлый месяц

        # c прошлого есть ссылка и можно перейти снова на текущий


        self.fail('Весь тест пока не выполняется')

    def tearDown(self):
        self.browser.quit()
        pass
