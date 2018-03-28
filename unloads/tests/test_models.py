import datetime

from django.test import TestCase

from unloads.models import Unload


# from django.utils import timezone


class UnloadModelTestCase(TestCase):

    def setUp(self):
        self.unload = Unload.objects.create(
            # date=timezone.now(),
            datetime=datetime.datetime(2017, 9, 1),
            him=3.5,
            water=100,
            cement=300,
            breakstone=1280,
            sand=700,
            is_active_left_bunker=True,
        )

    def test_unload_basic(self):
        """
        Test the basic functionality of Unload
        """
        self.assertEqual(self.unload.cement, 300)
        self.assertEqual(
            self.unload.datetime,
            datetime.datetime.strptime('01.09.2017', '%d.%m.%Y'),
        )
