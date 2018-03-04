# import datetime
#
# from django.test import LiveServerTestCase
#
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
#
# from unloads.models import Unload
#
#
# class UnloadsTestCase(LiveServerTestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(2)
#
#         self.unload1 = Unload.objects.create(
#             date=datetime.date(2017, 9, 1),
#             him=4,
#             water=100,
#             cement=400,
#             breakstone=1280,
#             sand=700,
#             is_active_left_bunker=True,
#         )
#
#         self.unload2 = Unload.objects.create(
#             date=datetime.datetime.strptime('01.09.2017', '%d.%m.%Y').date(),
#             him=3.5,
#             water=150.0,
#             cement=200.0,
#             breakstone=1000,
#             sand=500,
#             is_active_left_bunker=False,
#         )
#
#         self.unload3 = Unload.objects.create(
#             date=datetime.datetime.now().date(),
#             him=0,
#             water=80,
#             is_active_left_bunker=True,
#         )
#
#     def find_search_results(self):
#         return self.browser.find_elements_by_css_selector('.unload-row a')
#
#     def test_view_unload(self):
#         """
#         Тест что пользователь мjжет просматривать отгрузки
#         :return:
#         """
#
#         home_page = self.browser.get(self.live_server_url + '/unload')
#
#         # brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
#         # self.assertEqual('РБУ', brand_element.text)
#
#         try:
#             brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
#         except NoSuchElementException:
#             return self.fail('Не открывается страница Выгрузок. На странице не найден элемент ".navbar-brand"')
#
#         self.assertEqual('РБУ', brand_element.text)
#
#         # На странице форма с выбором даты
#         date_input = self.browser.find_element_by_css_selector(
#             'input#unload-date'
#         )
#         self.assertIsNotNone(self.browser.find_element_by_css_selector(
#             'label[for="unload-date"]'))
#         self.assertEqual(date_input.get_attribute('placeholder'),
#                          '22.03.1981')
#
#         # и общим списком отгрузок за сегодня
#         search_results = self.find_search_results()
#         # self.assertGreater(len(search_results), 1)
#         self.assertEqual(len(search_results), 1)
#
#         # Можно выбрать дату и отправить запрос
#         date_input.send_keys('01.09.2017')
#         # date_input.submit()
#         self.browser.find_element_by_css_selector('form button').click()
#
#         # И увидеть результат... отгрузки за дату
#         search_results = self.find_search_results()
#         self.assertGreater(len(search_results), 1)
#
#         # Можно выбрать отгрузку
#         search_results[0].click()
#
#         # На странице отгрузки увидеть дату,тип отгрузки, объём,
#         # количество компонентов, активный бункер и машину
#
#         self.assertEqual(
#             self.browser.current_url,
#             '{}/unload/1/'.format(self.live_server_url)
#         )
#
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-date').text,
#             '01.09.2017'
#         )
#
#         # На странице отгрузки увидеть тип отгрузки и количество таких отгрузок за этот день
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-type').text,
#             'None'
#         )
#
#         # На странице отгрузки увидеть объём и количество таких отгрузок за этот день
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-value').text,
#             'None'
#         )
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-him').text,
#             '4,0'
#         )
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-water').text,
#             '100,0'
#         )
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-cement').text,
#             '400,0'
#         )
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-breakstone').text,
#             '1280'
#         )
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-sand').text,
#             '700'
#         )
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-is_active_left_bunker').text,
#             'True'
#         )
#
#         # На странице отгрузки увидеть машину и количество-кубатуру таких отгрузок этой машины
#         self.assertEqual(
#             self.browser.find_element_by_css_selector('#unload-carrier').text,
#             'None'
#         )
#
#         # а также начальное и конечное время, количество приклеплённых статусов
#
#         # self.fail('Весь тест пока не выполняется')
#
#     def tearDown(self):
#         self.browser.quit()
#         pass
