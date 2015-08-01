

from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth import get_user_model


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

    def wait_for_element_with_class_name(self, class_name, timeout=15):
        WebDriverWait(self.browser, timeout).\
            until(lambda b: b.find_element_by_class_name(class_name),
                  'Element with class name: {} could not be found'.format(class_name))

    def get_body_content(self):
        return self.browser.find_element_by_tag_name('body').text

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

    def pre_login(self, live_server_url):
        user = get_user_model().objects.create_user(email='selenium_user@gmail.com',
                                                    first_name='selenium_user', password='pass1')
        self.browser.get('%s/account/selenium-login/?email=%s&password=%s' % (live_server_url, user.email, 'pass1'))
