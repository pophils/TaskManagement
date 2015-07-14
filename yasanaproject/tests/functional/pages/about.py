

from django.test import LiveServerTestCase
from selenium import webdriver


class AboutPage(object):

    def __init__(self, test_case):
        if not isinstance(test_case, LiveServerTestCase):
            raise TypeError('Constructor expecting a LiveServerTestCase instance')
        self.__testcase = test_case
        self.browser = None

    def load_new_browser_session(self):
        if self.browser is not None:
            self.browser.quit()

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def visit_about_page(self):
        self.load_new_browser_session()
        self.browser.get(self.__testcase.live_server_url + '/about')
        return self  # done to aid method chaining

    def has_right_title(self, title, browser):
        if browser is not None:
            self.browser = browser
        self.__testcase.assertIn(title, self.browser.title.lower())
