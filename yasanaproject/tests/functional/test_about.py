
from django.test import LiveServerTestCase
from .pages.about import AboutPage
from selenium import webdriver


class AboutViewTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(30)
        self.browser.maximize_window()

    def tearDown(self):
        if self.page:
            self.page = None
        self.browser.quit()

    def test_about_page_load_on_visit(self):

        self.page = AboutPage(self.browser)
        self.page.first_visit(self.live_server_url + '/about', 'about_welcome')

        self.assertEqual(self.browser.title.lower(), 'yasana --- about us')
        self.assertEqual(self.browser.find_element_by_id('about_welcome').text,
                         'We are African first Enterprise social network')
