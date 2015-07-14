
from django.test import LiveServerTestCase
from .pages.landing import LandingPage


class LandingViewTestCase(LiveServerTestCase):

    def setUp(self):
        self.page = LandingPage(self)

    def tearDown(self):
        if self.page is not None:
            self.page = None

    def test_user_interaction_on_landing(self):
        self.page = LandingPage(self)

        self.page.visit_landing_page()

        self.assertIn('yasana', self.page.browser.title.lower())

        about_page = self.page.visit_about_page()

        about_page.has_right_title('about', self.page.browser)




