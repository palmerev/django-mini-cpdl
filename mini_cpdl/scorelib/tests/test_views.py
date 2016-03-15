from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet

from scorelib.views import index
from scorelib.models import Score


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.piece1 = Score.objects.create(
            composer='John Dowland',
            voicing='SATB',
            title='Some Dowland Piece'
        )
        self.piece2 = Score.objects.create(
            composer='Anonymous',
            voicing='SSA',
            title='Ave Maria'
        )

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
            {'voicing': 'SATB'}
        )
        scores = response.context['scores']
        self.assertIs(type(scores), QuerySet)
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0].composer, 'John Dowland')
