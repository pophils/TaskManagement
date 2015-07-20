

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from .page_exception import PageException
from .base_page import BasePage


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

    def fill_login_form(self):
        email_field = self.browser.find_element_by_id('email')
        if not self.is_element_visible_and_enabled(email_field):
            raise PageException('Email field not found on login page.')

        password_field = self.browser.find_element_by_name('password')
        if not self.is_element_visible_and_enabled(password_field):
            raise PageException('Password field not found on login page.')

        submit_field = self.browser.find_element_by_id('submit-btn')
        if not self.is_element_visible_and_enabled(submit_field):
            raise PageException('Submit field not found on login page.')







    # def visit_index_page(self, url, element_id_to_wait_for):
    #     if not isinstance(url, str):
    #         raise TypeError('url is of type {}, expected str'. format(type(url)))
    #
    #     self.browser.get(url)
    #     self.wait_for_element_with_id('login-form')
    #     return self  # done to aid method chaining

    # def visit_about_page(self):
    #     about_us_link = self.browser.find_element_by_id('about-us')
    #     self.is_element_visible_and_enabled(about_us_link)
    #     about_us_link.click()
    #     return AboutPage(about_us_link.)
