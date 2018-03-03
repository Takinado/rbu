import os
from datetime import datetime

from django.test import TestCase

from rbu.settings import BASE_DIR
from statuses.models import Status, parsing_csv


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
            '18.01.2018 14:10:43', '845', '845', '1531', '3774', '1338', '1338', '1338',
            'BETONPC-beton-Log_file(2018-01-21_11-03-12)_files\\I43118_5907779282.jpg',
            'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'O', 'C', 'O', 'O', 'C', 'C',
            'L', 'H', 'F', 'N', 'U', 'e'
        ]

        self.status, created, error = Status.create(line)
        self.status2, created, error = Status.create(line2)
        self.lines = parsing_csv(
            os.path.join(BASE_DIR, 'test_data', 'BETONPC-beton-Log_file(2018-01-21_11-03-12).csv')
        )

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
            self.status.calculate_status(),
            self.status2,
        )

    def test_previous_status_not_exist(self):
        self.assertIsNone(
            self.status2.calculate_status()
        )

    def test_parsing_csv(self):
        print(self.lines[0])
        self.status3, created, error = Status.create(self.lines[0])
        self.assertEqual(
            self.status3,
            self.status2,
        )
