import os
from datetime import datetime

from django.test import TestCase

from rbu.settings import BASE_DIR
from statuses.models import (
    Status,
    parsing_csv,
    calculate_all_statuses,
    count_uncalculated_statuses
)


class StatusModelTestCase(TestCase):

    def setUp(self):
        fulldate = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
        line = [
            fulldate, '0', '0', '0', '0', '0', '0', '0',
            'BETONPC-beton-Log_file(2017-08-07_10-38-52)_files\\I42954_4381442708.jpg',
            'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'L', 'N', 'H', 'N', 'e', 'C'
        ]
        line2 = [
            '21.01.2018 11:07:24', '478', '478', '95', '686', '62', '62', '62',
            'BETONPC-beton-Log_file(2018-01-21_11-18-25)_files\\I43121_4634793634.jpg',
            'C', 'C', 'C', 'O', 'C', 'C', 'C',
            'C', 'C', 'C', 'C', 'C', 'O', 'C',
            'O', 'C', 'C', 'C',
            'L', 'H', 'F', 'N', 'e', 'O'
        ]

        self.status, created, error = Status.create(line)
        self.status2, created, error = Status.create(line2)
        self.lines = parsing_csv(
            os.path.join(BASE_DIR, 'test_data', 'BETONPC-beton-Log_file(2018-01-21_11-18-25).csv')
        )
        # self.lines += parsing_csv(
        #     os.path.join(BASE_DIR, 'test_data', 'BETONPC-beton-Log_file(2018-01-21_11-33-25).csv')
        # )
        # self.lines += parsing_csv(
        #     os.path.join(BASE_DIR, 'test_data', 'BETONPC-beton-Log_file(2018-01-21_11-48-25).csv')
        # )
        # self.lines += parsing_csv(
        #     os.path.join(BASE_DIR, 'test_data', 'BETONPC-beton-Log_file(2018-01-21_12-03-25).csv')
        # )
        for line in self.lines:
            Status.create(line)

    def test_status_basic(self):
        """
        Тест базовой функциональности Status
        """
        self.assertEqual(self.status.cement, 0)
        self.assertEqual(self.status.warning, False)
        self.assertEqual(
            self.status.date,
            datetime.now().date(),
        )

    def test_previous_status_exist(self):
        self.assertEqual(
            self.status.get_previous().datetime,
            datetime(2018, 1, 21, 11, 13, 26),
        )

    def test_previous_status_not_exist(self):
        self.assertEqual(
            self.status2.get_previous(),
            self.status2
        )

    def test_parsing_csv(self):
        self.status3, created, error = Status.create(self.lines[0])
        self.assertEqual(
            self.status3,
            self.status2,
        )

    def test_total_statuses(self):
        total_statuses = Status.objects.all().count()
        self.assertEqual(
            total_statuses,
            9,
        )

    def test_all_statuses_calculated(self):
        self.assertEqual(
            count_uncalculated_statuses(),
            9
        )
        calculate_all_statuses()
        self.assertEqual(
            count_uncalculated_statuses(),
            0
        )
