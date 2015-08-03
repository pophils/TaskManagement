

from .page_exception import PageException
from .base_page import BasePage
from .landing import LandingPage


class LoginPage(BasePage):

    def __init__(self, browser):
        super().__init__(browser)
        self.load_browser_if_none()

    def validate_page(self):
        try:
            self.browser.find_element_by_id('login-header-title')
            self.browser.find_element_by_id('login-form')
        except:
            raise PageException('Login page not loaded')

    def login_user(self, email, password):
        email_field = self.browser.find_element_by_id('email')
        if not self.is_element_visible_and_enabled(email_field):
            raise PageException('Email field not found on login page.')

        password_field = self.browser.find_element_by_name('password')
        if not self.is_element_visible_and_enabled(password_field):
            raise PageException('Password field not found on login page.')

        submit_field = self.browser.find_element_by_id('submit-btn')
        if not self.is_element_visible_and_enabled(submit_field):
            raise PageException('Submit field not found on login page.')

        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_field.click()

        self.wait_for_element_with_id('dashboard-link', 5)

        return LandingPage(self.browser)
