
from .page_exception import PageException
from .base_page import BasePage


class LandingPage(BasePage):

    def __init__(self, browser):
        super().__init__(browser)
        self.load_browser_if_none()

    def validate_page(self):
        try:
            self.browser.find_element_by_id('landing-welcome')
        except:
            raise PageException('Landing page not loaded')

    def task_summary_p_tag_count(self):
        p_summary_count = self.browser.find_elements_by_class_name('summary-count')
        return len(p_summary_count)

    def get_nav_link_first_item_text(self):
        return self.browser.find_element_by_css_selector('li.active').text
