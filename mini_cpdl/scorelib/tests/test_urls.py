from django.test import TestCase
from django.core.urlresolvers import resolve

from scorelib.views import index


class ScorelibURLsTestCase(TestCase):

    def test_root_url_uses_index_view(self):
        """Test that the root of the site resolves to the correct view"""
        root = resolve('/')
        self.assertEqual(root.func, index)

    def test_score_detail_url(self):
        """Test that the URL for ScoreDetail resolves to the correct view"""
        score_detail = resolve('/scores/1/')

        self.assertEqual(score_detail.func.__name__, 'ScoreDetailView')
        self.assertEqual(score_detail.kwargs['pk'], '1')
