

from django.test import TestCase
from django.core.exceptions import ValidationError
from yasana.models.organisation import Organisation


class OrganisationTestCase(TestCase):

    def test_organisation_can_save(self):

        first_org = Organisation.objects.create(name='Allied soft', address='61/62, Kingsway building, Marina Lagos.')
        sec_org = Organisation.objects.create(name='Verite MFB', address='66, Kingsway building, Marina Lagos.')

        saved_organisations = Organisation.objects.all()

        self.assertEqual(saved_organisations.count(), 2, 'Organisation save error.')
        self.assertEqual(first_org.name, saved_organisations[0].name)
        self.assertEqual(sec_org.name, saved_organisations[1].name)

    def test_invalid_organisation_raise_validation_error(self):

        with self.assertRaises(ValidationError):
            org = Organisation.objects.create(name='', address='61/62, Kingsway building, Marina Lagos.')
            org.full_clean()  # Used to hack around sqllite db level validation problem e.g with empty string

        with self.assertRaises(ValidationError):
            org = Organisation.objects.create(name='Allied soft limited', address='')
            org.full_clean()  # Used to hack aroud sqllite db level validation problem e.g with empty string




