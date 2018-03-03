# from datetime import datetime
#
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
#
# from statuses.models import Status
# from statuses.views import import_csv_view
#
#
# class StatusTestCase(LiveServerTestCase):
#
#     # запускается для каждого теста
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(2)
#
#         # import_all_csv()
#
#         fulldate = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
#         line = [
#             fulldate, '0', '0', '0', '0', '0', '0', '0',
#             'BETONPC-beton-Log_file(2017-08-07_10-38-52)_files\\I42954_4381442708.jpg',
#             'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
#             'L', 'N', 'H', 'N', 'e', 'C'
#         ]
#         self.status1, created, error = Status.create(line)
#
#     def find_search_results(self):
#         return self.browser.find_elements_by_css_selector('.status-row a')
#
#     def test_view_status(self):
#         """
#         Тест что пользователь может просматривать статусы
#         :return:
#         """
#
#         home_page = self.browser.get(self.live_server_url + '/status')
#
#         try:
#             brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
#         except NoSuchElementException:
#             return self.fail('Не открывается страница Статусов. На странице не найден элемент ".navbar-brand"')
#
#         self.assertEqual('РБУ', brand_element.text)
#
#         # На странице форма с выбором даты
#         date_input = self.browser.find_element_by_css_selector(
#             'input#status-date'
#         )
#         self.assertIsNotNone(self.browser.find_element_by_css_selector(
#             'label[for="status-date"]'))
#         self.assertEqual(date_input.get_attribute('placeholder'),
#                          '21.01.2018')
#
#         # и общим списком статусов за сегодня
#         search_results = self.find_search_results()
#         # self.assertEqual(len(search_results), 1)
#         self.assertGreaterEqual(len(search_results), 1)
#
#         # Можно выбрать дату и отправить запрос
#         date_input.send_keys('21.01.2018')
#         self.browser.find_element_by_css_selector('form button').click()
#
#         # И увидеть результат... статусы за дату
#         search_results = self.browser.find_elements_by_css_selector('.status-row td:nth-child(2) a')
#         self.assertEqual(len(search_results), 2)
#
#         # Можно выбрать статус
#         search_results[0].click()
#
#         # На странице отгрузки увидеть дату, время и все данные из модели
#         # Числом статусов: общим, с ошибками, с предупреждениями, не посчитаных, без отгрузки
#         # а также модель фото и если нужно фото
#         # ссылку на отгрузку
#         date_url = datetime.strftime(datetime.now(), "%Y/%m/%d")
#
#         self.assertEqual(
#             self.browser.current_url,
#             '{}/status/12/'.format(self.live_server_url)
#         )
#
#         try:
#             brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
#         except NoSuchElementException:
#             return self.fail('Не открывается страница Статуса. На странице не найден элемент ".navbar-brand"')
#
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#status-date').text,
#             '21.01.2018'
#         )
#
#         # проверка что активный бункер левый
#         self.assertEqual(self.status1.rbu_statuses.cem_bunker_active,
#                          'L')
#
#         # self.fail('Весь тест пока не выполняется')
#
#     # def test_pars_cem_bunker_active(self):
#     #     self.assertEqual(self.status1.rbu_statuses.cem_bunker_active,
#     #                      'L')
#
#     def tearDown(self):
#         self.browser.quit()
#         pass
