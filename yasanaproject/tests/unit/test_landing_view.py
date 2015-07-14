

from django.test import TestCase
from django.core.urlresolvers import resolve
from yasana.controller.landing import LandingView


class LandingViewTestCase(TestCase):

    def test_landing_url_resolve_properly(self):
        resolved_url = resolve('/')

        self.assertEqual(resolved_url.func.__name__, LandingView.as_view().__name__, msg='Landing url resolve fails')

    def test_landing_get_returns_right_template(self):

        response = self.client.get('/')

        self.assertTemplateUsed(response, 'yasana/landing.html')

    def test_landing_get_contains_yasana_in_title(self):
        response = self.client.get('/')
        self.assertContains(response, 'yasana')
