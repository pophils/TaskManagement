

from django.test import TestCase
from django.core.urlresolvers import resolve
from yasana.controller.about import AboutView


class AboutViewTestCase(TestCase):

    def test_about_url_resolve_properly(self):
        resolved_url = resolve('/about/')

        self.assertEqual(resolved_url.func.__name__, AboutView.as_view().__name__, msg='About url resolve fails')

    def test_about_get_returns_right_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'yasana/about.html')
