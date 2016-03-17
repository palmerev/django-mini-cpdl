from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet

from scorelib.views import index, ScoreDetailView
from scorelib.models import Score


class ScorelibBaseTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        # this calls inherited django code that uses setUpClass itself
        super().setUpClass()
        cls.piece1 = Score.objects.create(
            composer='John Dowland',
            voicing='SATB',
            title='Some Dowland Piece'
        )
        cls.piece2 = Score.objects.create(
            composer='Anonymous',
            voicing='SSA',
            title='Ave Maria'
        )


class IndexViewTestCase(ScorelibBaseTestCase):
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


class ScoreViewTestCase(ScorelibBaseTestCase):
    def test_basic(self):
        """Test the the score view returns a 200 response,
            uses correct template, and has the correct context"""
        request = self.factory.get('/solos/1/')

        response = ScoreDetailView.as_view()(
            request,
            self.piece1.pk
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['score'].composer,
            'Anonymous'
        )
        with self.assertTemplateUsed('scorelib/score_detail.html'):
            response.render()
