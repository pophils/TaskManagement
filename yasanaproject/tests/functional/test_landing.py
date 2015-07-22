
from django.test import LiveServerTestCase
from .pages.landing import LandingPage
from selenium import webdriver
from unittest import skip


class LandingViewTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(30)
        self.browser.maximize_window()

    def tearDown(self):
        if self.page:
            self.page = None
        self.browser.quit()

    def test_anonymous_user_redirected_to_login_page_on_visit(self):
        self.page = LandingPage(self.browser)

        self.page.first_visit(self.live_server_url)

        self.assertEqual(self.browser.title.lower(), 'yasana -- login')

    def test_logged_in_user_is_not_redirected_to_login_page_on_visit(self):

        self.page = LandingPage(self.browser)

        self.page.pre_login(self.live_server_url)

        self.page.first_visit(self.live_server_url)

        self.assertEqual(self.browser.title.lower(), 'yasana --- enterprise social network.')
