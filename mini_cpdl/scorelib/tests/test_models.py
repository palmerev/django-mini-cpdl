from django.test import TestCase

from scorelib.models import Score


class ScoreModelTestCase(TestCase):

    def setUp(self):
        self.score = Score.objects.create(
            title='Come Again, Sweet Love',
            composer='John Dowland',
            voicing='SATB'
        )

    def test_score_basic(self):
        """Test the basic functionality of Score"""
        self.assertEqual(self.score.composer, 'John Dowland')
