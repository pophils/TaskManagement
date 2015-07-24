
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .pages.landing import LandingPage
from selenium import webdriver
from unittest import skip


class LandingViewTestCase(StaticLiveServerTestCase):

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

    def test_logged_in_user_can_see_task_summary(self):

        self.page = LandingPage(self.browser)

        self.page.pre_login(self.live_server_url)

        self.page.first_visit(self.live_server_url)

        p_summary_count = self.page.task_summary_p_tag_count()

        self.assertTrue(p_summary_count >= 3)

    def test_logged_in_user_can_see_necessary_nav_links(self):

        self.page = LandingPage(self.browser)

        self.page.pre_login(self.live_server_url)

        self.page.first_visit(self.live_server_url)

        li_item_text = self.page.get_nav_link_first_item_text()

        self.assertIn('dashboard', li_item_text.lower())



