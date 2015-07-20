
from django.test import LiveServerTestCase
from .pages.landing import LandingPage
from .pages.login import LoginPage
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

    @skip
    def test_logged_in_user_is_not_redirected_to_login_page_on_visit(self):

        self.page = LandingPage(self.browser)
        self.page.pre_create_user_session('user1@gmail.com', 'user1', 'pass1', self.live_server_url + '/404_session')

        self.page.first_visit(self.live_server_url)

        # self.assertEqual(self.browser.title.lower(), 'yasana --- Enterprise social network.')

    @skip
    def test_user_interaction_on_landing(self):

        self.page = LandingPage(self.browser)

        self.assertIn('yasana', self.page.browser.title.lower())

        # about_page = self.page.visit_about_page()

        # about_page.has_right_title('about', self.page.browser)






