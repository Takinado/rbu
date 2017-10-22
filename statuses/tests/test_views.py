from datetime import datetime

from django.db.models import QuerySet
from django.test import TestCase, RequestFactory

from statuses.models import Status
from statuses.views import index_statuses_view, StatusDayView, StatusDetailView, import_one_csv


class StatusBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # fulldate = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
        # line = [
        #     fulldate, '0', '0', '0', '0', '0', '0', '0',
        #     'BETONPC-beton-Log_file(2017-08-07_10-38-52)_files\\I42954_4381442708.jpg',
        #     'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
        #     'L', 'N', 'H', 'N', 'e', 'C'
        # ]
        # cls.status1, created = Status.create(line)
        #
        # print(cls.status1)
        #
        # statuses = import_one_csv(debug=True)


class IndexUnloadViewTestCase(StatusBaseTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        fulldate = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
        line = [
            fulldate, '0', '0', '0', '0', '0', '0', '0',
            'BETONPC-beton-Log_file(2017-08-07_10-38-52)_files\\I42954_4381442708.jpg',
            'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'L', 'N', 'H', 'N', 'e', 'C'
        ]
        self.status4, created = Status.create(line)
        statuses = import_one_csv(debug=True)

    def test_index_status_view_basic(self):
        """
        Тест что представление за сегодня возвращает 302
        """
        request = self.factory.get('/status/')
        response = index_statuses_view(request)
        self.assertEqual(response.status_code, 302)

    def test_status_list_view_from_index_basic(self):
        """
        Тест что представление при перенаправлении с главной страницы статусов возвращает 200
        и использует правильный шаблон
        """
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        day = str(datetime.now().day)

        request = self.factory.get('/status/{}/{}/{}/'.format(year, month, day))
        response = StatusDayView.as_view()(request, year=year, month=month, day=day)

        with self.assertTemplateUsed('statuses/status_archive_day.html'):
            response.render()

        response2 = StatusDayView.as_view()(request, year=year, month=month, day=day)
        self.assertEqual(response2.status_code, 200)

        response3 = StatusDayView.as_view()(request, year=year, month=month, day=day)
        with self.assertTemplateUsed('statuses/status_archive_day.html'):
            response3.render()
            self.assertEqual(response3.status_code, 200)

    def test_status_list_view_basic(self):
        """
        Тест что представление статусов за дату возвращает 200
        и использует правильный шаблон
        """
        year = '2017'
        month = '8'
        day = '7'

        request = self.factory.get('/status/{}/{}/{}/'.format(year, month, day))
        response = StatusDayView.as_view()(request, year=year, month=month, day=day)

        with self.assertTemplateUsed('statuses/status_archive_day.html'):
            response.render()
            self.assertEqual(response.status_code, 200)

    # def test_index_status_view_returns_statuses(self):
    #     """
    #     Тест что представление может возвращать список статусов,
    #     если получает запрос
    #     """
    #     test_date = '2017/08/07'
    #     test_date = '07.08.2017'
    #     response = self.client.get(
    #         "/status/",
    #         {'date': test_date}
    #     )
    #
    #     print(response.context)
    #
    #     status_list = response.context['status_list']
    #
    #     self.assertIs(type(status_list), QuerySet)
    #     self.assertGreaterEqual(len(status_list), 1)
    #     self.assertEqual(status_list[0].him, 4)


# class UnloadViewTestCase(StatusBaseTestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_basic(self):
#         """
#         Тестирование того что status_view возращает 200,
#         использует правильный шаблон и правильный контекст
#         :return:
#         """
#         request = self.factory.get('/status/1/')
#
#         response = StatusDetailView.as_view()(
#             request,
#             pk=self.status1.pk
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.context_data['status'].date, datetime.date(2017, 9, 1)
#         )
#         with self.assertTemplateUsed('statuses/status_detail.html'):
#             response.render()
