
import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .pages.login import LoginPage


class ManageUserTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(20)
        self.browser.maximize_window()

    def tearDown(self):
        if self.browser:
            self.browser = None

    def test_user_interaction_on_manage_user_page(self):
        temp_page = LoginPage(self.browser)
        temp_page.first_visit('{}/account/login/'.format(self.live_server_url), 'email')
        temp_page = temp_page.login_user('admin@admin.com', 'admin')

        temp_page.first_visit(self.live_server_url)
        self.page = temp_page.visit_manage_user()

        self.assertIn('Manage Users', self.page.get_body_content())
        user_info = self.page.add_new_user()

        self.page.wait_for_element_with_class_name('stickit_name')
        tbody = self.browser.find_element_by_id('tbody')
        tbody_text = tbody.text.lower()

        email = user_info.get('email').lower()
        name = user_info.get('name').lower()
        phone = user_info.get('phone').lower()
        department = user_info.get('department').lower()

        self.assertIn(email, tbody_text)
        self.assertIn(name, tbody_text)
        self.assertIn(phone, tbody_text)
        self.assertIn(department, tbody_text)

        edited_user_info = self.page.edit_user()

        self.page.wait_for_element_with_class_name('stickit_name')
        tbody = self.browser.find_element_by_id('tbody')
        tbody_text = tbody.text.lower()

        self.assertNotIn(name, tbody_text)
        self.assertNotIn(phone, tbody_text)
        self.assertNotIn(department, tbody_text)

        self.assertIn(edited_user_info.get('name').lower(), tbody_text)
        self.assertIn(edited_user_info.get('phone').lower(), tbody_text)
        self.assertIn(edited_user_info.get('department').lower(), tbody_text)

        self.page.delete_user()

        time.sleep(3)

        tbody = self.browser.find_element_by_id('tbody')
        tbody_text = tbody.text.lower()

        self.assertNotIn(edited_user_info.get('name').lower(), tbody_text)
        self.assertNotIn(edited_user_info.get('phone').lower(), tbody_text)
        self.assertNotIn(edited_user_info.get('department').lower(), tbody_text)
        self.assertNotIn(email, tbody_text)
