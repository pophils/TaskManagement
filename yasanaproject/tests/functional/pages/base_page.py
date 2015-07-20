

from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.conf import settings
from ...utils.db import create_pre_authenticated_session
from .page_exception import PageException


class BasePage(object):

    def __init__(self, browser):
        if not isinstance(browser, webdriver.Firefox):
            raise TypeError('browser passed is of {} type. Constructor expecting webdriver instance.'.
                            format(type(browser)))

        self.browser = browser

    @abstractmethod
    def validate_page(self):
        pass

    def first_visit(self, url, element_id_to_wait_for=None):
        if not isinstance(url, str):
            raise TypeError('url is of type {}, expected str'. format(type(url)))

        self.browser.get(url)
        if element_id_to_wait_for:
            self.wait_for_element_with_id(element_id_to_wait_for)

        return self  # done to aid method chaining

    def wait_for_element_with_id(self, element_id, timeout=15):
        WebDriverWait(self.browser, timeout).\
            until(lambda b: b.find_element_by_id(element_id),
                  'Element with id: {} could not be found'.format(element_id))

    @staticmethod
    def is_element_visible(element):
        return element.is_displayed()

    @staticmethod
    def is_element_enabled(element):
        return element.is_enabled()

    @staticmethod
    def is_element_visible_and_enabled(element):
        return element.is_displayed() and element.is_enabled()

    def load_browser_if_none(self):
        if self.browser is None:
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(30)
            self.browser.maximize_window()

    def pre_create_user_session(self, email, first_name, password, wrong_url):
        # load a 404 not found page to help in storing session
        if not wrong_url or not isinstance(wrong_url, str):
            raise PageException('Please pass a wrong url to help in pre creating session.')

        self.browser.get(wrong_url)
        dd = create_pre_authenticated_session(email, first_name, password)
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=dd,
                path='/',)
        )
