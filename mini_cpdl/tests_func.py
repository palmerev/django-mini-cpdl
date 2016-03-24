
from selenium import webdriver
from unittest import skip

from django.test import LiveServerTestCase

from scorelib.models import Score


class BaseMusicianTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(2)

        cls.score1 = Score.objects.create(
            composer='Orlando di Lasso',
            voicing='SATB',
            title='An SATB Lasso Piece'
        )
        cls.score2 = Score.objects.create(
            composer='Orlando di Lasso',
            voicing='SATB',
            title='Another SATB Lasso Piece'
        )
        cls.score3 = Score.objects.create(
            composer='Orlando di Lasso',
            voicing='SSATB',
            title='A Five-Part Lasso Piece'
        )

    @classmethod
    def tearDown(cls):
        del cls.score1
        del cls.score2
        del cls.score3
        cls.browser.quit()


class MusicianTestCase(BaseMusicianTestCase):

    def find_search_results(self):
        return self.browser.find_elements_by_css_selector(
            '.scorelib-search-result a')

    def test_musician_can_find_a_piece(self):
        """Test that a user can search for pieces"""
        # Carolyn is a singer who would like to find some peices to sing with
        # her friends. She visits the home page of miniScoreLib.
        home_page = self.browser.get(self.live_server_url + '/')
        # She knows she's in the right place because she can see the name of the
        # site in the browser chrome.
        brand_element = self.browser.find_element_by_css_selector(
            '.navbar-brand')
        self.assertEqual('miniScoreLib', brand_element.text)
        # She sees the inputs of the search form, including labels
        # and placeholders.
        composer_input = self.browser.find_element_by_css_selector(
            'input#composer-field')
        self.assertIsNotNone(self.browser.find_element_by_css_selector(
            'label[for="composer-field"]'))
        self.assertEqual(composer_input.get_attribute('placeholder'),
            'i.e. Byrd')
        voicing_input = self.browser.find_element_by_css_selector(
            'input#voicing-field')
        self.assertIsNotNone(self.browser.find_element_by_css_selector(
            'label[for="voicing-field"]'))
        self.assertEqual(
            voicing_input.get_attribute('placeholder'), 'i.e. SATB')

        # She types in the name of a composer, and submits it.
        composer_input.send_keys('Lasso')
        self.browser.find_element_by_css_selector('form button').click()
        # She sees too many search results...
        search_results = self.find_search_results()
        self.assertGreater(len(search_results), 2)
        # ...so she adds a voicing to her search query and gets a more
        # manageable list.
        voicing_input = self.browser.find_element_by_css_selector(
            'input#voicing-field')
        voicing_input.send_keys('SATB')
        self.browser.find_element_by_css_selector('form button').click()
        search_results2 = self.find_search_results()
        self.assertEqual(len(search_results2), 2)
        # She clicks on a search result.
        search_results2[1].click()
        # The piece's page has the title, composer, and voicing of
        # the piece.
        self.assertEqual(
            self.browser.current_url,
            '{}/scores/2/'.format(self.live_server_url)
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector('#score-detail-title').text,
            'Another SATB Lasso Piece'
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector('#score-detail-voicing').text,
            'SATB'
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector('#score-detail-composer').text,
            'Orlando di Lasso'
        )

    @skip('not ready for this yet')
    def test_musician_can_create_collections(self):
        """Test that if the user clicks on the 'Add to collection' button,
        they will be prompted to create one if they don't already have one,
        or prompted to choose one from a list."""

        # From the score detail page
        score_page = self.browser.get('/{}/scores/2/'.format(self.live_server_url))
        # She sees a button labeled 'New collection',
        self.assertEqual(self.browser.find_element_by_css_selector(
            '#scorelib-new-collection-btn').text,
            'New collection'
        )
        self.fail('Incomplete test')
        # She clicks the 'New collection' button

        # A modal appears saying 'You don't have any collections'

        # The modal also includes an input field that's labeled:
        # 'Enter name for new collection', and a 'Create' button

        # She enters 'SATB Italian Madrigals' and clicks 'Create'

        # She sees the 'You don't have any collections' text replaced by the
        # name of her new collection

        # She clicks the 'X' in the upper right-hand corner of the modal, and
        # the modal disappears

        # She notices that a new button has appeared on the page that says
        # 'Add to collection'

        # She clicks 'Add to collection', and another modal appears titled
        # 'Add "Another SATB Lasso Piece" to...', and listing her
        # 'SATB Italian Madrigals' collection

        # She clicks on the name of her collection and is notified that
        # the piece has been added to the collection

        # Satisfied, she clicks the 'X' in the upper right-hand corner of
        # the modal, and it disappears

    @skip('not written yet')
    def test_musician_can_modify_to_collection(self):
        pass
