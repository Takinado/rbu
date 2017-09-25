from datetime import datetime

from django.test import TestCase

from statuses.models import Status


class StatusModelTestCase(TestCase):

    def setUp(self):
        fulldate = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
        line = [
            fulldate, '0', '0', '0', '0', '0', '0', '0',
            'BETONPC-beton-Log_file(2017-08-07_10-38-52)_files\\I42954_4381442708.jpg',
            'C', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'L', 'N', 'H', 'N', 'e', 'C'
        ]
        self.status, created = Status.create(line)

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
