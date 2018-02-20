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
            '01.12.2017 6:43:57', '452', '452', '804', '636', '410', '410', '410',
            'BETONPC-beton-Log_file(2017-12-01_06-47-30)_files\\I43070_2805251389.jpg',
            'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'O', 'C', 'O', 'C', 'C', 'C',
            'L', 'H', 'H', 'N', 'e', 'C'
        ]
        self.status, created = Status.create(line)
        self.status2, created = Status.create(line2)
        self.lines = parsing_csv(
            os.path.join(BASE_DIR, 'test_data', 'BETONPC-beton-Log_file(2017-12-01_06-47-30).csv')
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
        self.status3, created = Status.create(self.lines[0])
        self.assertEqual(
            self.status3,
            self.status2,
        )
