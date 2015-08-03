

from .page_exception import PageException
from .base_page import BasePage
from selenium.webdriver.support.select import Select


class ManageUserPage(BasePage):

    def validate_page(self):
        pass

    def __init__(self, browser):
        super().__init__(browser)
        self.load_browser_if_none()

    def add_new_user(self):
        add_user_btn = self.browser.find_element_by_id('new-user-btn')
        add_user_btn.click()

        self.wait_for_element_with_id('first_name', timeout=10)
        popup = self.browser.find_element_by_class_name('popup-wrap')

        first_name_field = popup.find_element_by_id('first_name')

        last_name_field = popup.find_element_by_id('last_name')

        other_name_field = popup.find_element_by_id('other_name')
        phone_field = popup.find_element_by_id('phone')
        website_field = popup.find_element_by_id('website')
        department_field = popup.find_element_by_id('department')
        email_field = popup.find_element_by_id('email')
        password_field = popup.find_element_by_id('password')
        confirm_password_field = popup.find_element_by_id('confirm_password')
        submit_user_field = popup.find_element_by_id('submit-user')
        gender_ddl = Select(popup.find_element_by_id('gender'))

        first_name_field.send_keys('blaise')
        last_name_field.send_keys('pascal')
        other_name_field.send_keys('adam')
        phone_field.send_keys('+234578362728')
        department_field.send_keys('Computing Network Team')
        website_field.send_keys('www.google.com')
        email_field.send_keys('blaise@gmail.com')
        password_field.send_keys('pass1')
        confirm_password_field.send_keys('pass1')
        gender_ddl.select_by_index(1)
        submit_user_field.click()

        return {'email': 'blaise@gmail.com', 'name': 'pascal, blaise adam', 'phone': '+234578362728',
                'department': 'Computing Network Team'}

    def edit_user(self):
        edit_user_btn = self.browser.find_element_by_css_selector('.btn.btn-primary')
        edit_user_btn.click()

        popup = self.browser.find_element_by_class_name('popup-wrap')

        first_name_field = popup.find_element_by_id('first_name')

        last_name_field = popup.find_element_by_id('last_name')

        other_name_field = popup.find_element_by_id('other_name')
        phone_field = popup.find_element_by_id('phone')
        department_field = popup.find_element_by_id('department')
        submit_user_field = popup.find_element_by_id('submit-user')
        gender_ddl = Select(popup.find_element_by_id('gender'))

        first_name_field.clear()
        first_name_field.send_keys('Clement')
        last_name_field.clear()
        last_name_field.send_keys('Edith')
        other_name_field.clear()
        other_name_field.send_keys('adam')
        phone_field.clear()
        phone_field.send_keys('09000675457')
        department_field.clear()
        department_field.send_keys('Machine Learning')
        gender_ddl.select_by_index(2)
        submit_user_field.click()

        return {'name': 'edith, clement adam', 'phone': '09000675457', 'department': 'Machine Learning'}

    def delete_user(self):
        edit_user_btn = self.browser.find_element_by_css_selector('.btn.btn-danger')
        edit_user_btn.click()
