from django.test import TestCase
from django.core.urlresolvers import resolve

from unloads.views import unload_list_view


class UnloadsURLTestCase(TestCase):

    def test_root_url_uses_unload_list_view(self):
        """
        Test that the unload_list_view of the site resolves to the
        correct view function
        """

        # brand_element = self.browser.find_element_by_css_selector('#unload-list-link')
        root = resolve('/unload/')
        self.assertEqual(root.func, unload_list_view)
