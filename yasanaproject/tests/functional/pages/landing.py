

from django.test import LiveServerTestCase
from selenium import webdriver
from .about import AboutPage


class LandingPage(object):

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

    def visit_landing_page(self):
        self.load_new_browser_session()
        self.browser.get(self.__testcase.live_server_url)
        return self  # done to aid method chaining

    def visit_about_page(self):
        about_us_link = self.browser.find_element_by_id('about-us')
        about_us_link.click()
        self.wait_for()
        return AboutPage(self.__testcase)

    def wait_for(self):
        self.browser.implicitly_wait(10)

