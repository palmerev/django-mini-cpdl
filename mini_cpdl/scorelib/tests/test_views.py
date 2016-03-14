from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet

from scorelib.views import index


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """Test that the index view returns a 200 response and
        uses the correct template"""
        request = self.factory.get('/')
        with self.assertTemplateUsed('scorelib/index.html'):
            response = index(request)
            self.assertEqual(response.status_code, 200)

    def test_index_view_returns_scores(self):
        """Test that the index view attempts to return Scores if query
        parameters exist"""
        # use the test client instead of factory so we can
        # access the response.context dictionary
        response = self.client.get(
            '/',
            {'composer': 'Dowland'}
        )
        self.assertIs(
            type(response.context['scores']),
            QuerySet
        )
