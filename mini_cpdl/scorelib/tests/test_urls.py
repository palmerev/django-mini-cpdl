from django.test import TestCase
from django.core.urlresolvers import resolve

from scorelib.views import index


class ScorelibURLsTestCase(TestCase):

    def test_root_url_uses_index_view(self):
        """Test that the root of the site resolves to the correct view"""
        root = resolve('/')
        self.assertEqual(root.func, index)
