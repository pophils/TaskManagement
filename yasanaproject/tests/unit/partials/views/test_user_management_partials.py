

from django.test import TestCase
from django.core.urlresolvers import resolve
from partials.controller.user_management import user_collection_partial, add_user_partial


class UserManagementPartialTestCase(TestCase):

    def test_user_collection_partial_resolve_correctly(self):
        resolved_func = resolve('/partials/user-collection/')

        self.assertEqual(resolved_func.func, user_collection_partial)

    def test_add_user_partial_resolve_correctly(self):
        resolved_func = resolve('/partials/add-user/')

        self.assertEqual(resolved_func.func, add_user_partial)

    def test_user_collection_partial_returns_right_template(self):
        response = self.client.get('/partials/user-collection/')

        self.assertTemplateUsed(response, 'partials/user_collection.html')

    def test_add_user_partial_returns_right_template(self):
        response = self.client.get('/partials/add-user/')

        self.assertTemplateUsed(response, 'partials/add_user.html')
