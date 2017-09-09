import datetime
from django.test import TestCase

from unloads.models import Unload


class UnloadModelTestCase(TestCase):

    def setUp(self):
        self.unload = Unload.objects.create(
            date=datetime.datetime.now(),
            cement=400,
        )

    def test_unload_basic(self):
        """
        Test the basic functionality of Unload
        """
        self.assertEqual(self.unload.cement, 400)
