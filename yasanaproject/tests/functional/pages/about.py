

from .page_exception import PageException
from .base_page import BasePage


class AboutPage(BasePage):

    def __init__(self, browser):
        super().__init__(browser)
        self.load_browser_if_none()

    def validate_page(self):
        try:
            self.browser.find_element_by_id('about_welcome')
        except:
            raise PageException('About page not loaded')
