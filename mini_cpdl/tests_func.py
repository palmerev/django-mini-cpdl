from django.test import LiveServerTestCase
from selenium import webdriver

from scorelib.models import Score


class MusicianTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        self.score1 = Score.objects.create(
            composer='Orlando di Lasso',
            voicing='SATB',
            title='An SATB Lasso Piece'
        )
        self.score2 = Score.objects.create(
            composer='Orlando di Lasso',
            voicing='SATB',
            title='Another SATB Lasso Piece'
        )
        self.score3 = Score.objects.create(
            composer='Orlando di Lasso',
            voicing='SSATB',
            title='A Five-Part Lasso Piece'
        )

    def tearDown(self):
        self.browser.quit()

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
        search_results = self.browser.find_elements_by_css_selector(
            '.scorelib-search-result')
        self.browser.implicitly_wait(1)
        self.assertGreater(len(search_results), 2)
        # ...so she adds a voicing to her search query and gets a more
        # manageable list.
        voicing_input = self.browser.find_element_by_css_selector(
            'input#voicing-field')
        voicing_input.send_keys('SATB')
        self.browser.find_element_by_css_selector('form button').click()
        search_results2 = self.browser.find_elements_by_css_selector(
            '.scorelib-search-result')
        self.assertEqual(len(search_results2), 2)
        result_links = self.browser.find_elements_by_css_selector(
            '.scorelib-search-result a'
        )
        self.assertEqual(len(result_links), 2)
        # She clicks on a search result.
        result_links[0].click()
        self.fail('Incomplete Test')
        # The piece's page has the title, composer, and voicing of
        # the piece.
        self.assertEqual(
            self.browser.current_url,
            '{}/scores/2/'.format(self.live_server_url0)
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector('#scorelib-title').text,
            'Another SATB Lasso Piece'
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector('#scorelib-voicing').text,
            'SATB'
        )
        # She also sees an option to bookmark this piece.
        self.assertEqual(self.browser.find_element_by_css_selector(
            '#scorelib-bookmark-btn').text,
            'Bookmark this piece'
        )
