import datetime

from django.test import TestCase
# from django.utils import timezone

from unloads.models import Unload


class UnloadModelTestCase(TestCase):

    def setUp(self):
        self.unload = Unload.objects.create(
            # date=timezone.now(),
            date=datetime.date(2017, 9, 1),
            cement=400,
        )

    def test_unload_basic(self):
        """
        Test the basic functionality of Unload
        """
        self.assertEqual(self.unload.cement, 400)
