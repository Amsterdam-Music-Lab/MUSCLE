from django.core.exceptions import ValidationError
from django.test import TestCase

from experiment.validators import block_slug_validator


class ExperimentValidatorsTest(TestCase):
    def test_valid_slug(self):
        # Test a valid lowercase slug
        slug = 'testslug'
        try:
            block_slug_validator(slug)
        except ValidationError:
            self.fail(f"Unexpected ValidationError raised for slug: {slug}")

    def test_disallowed_slug(self):
        # Test a disallowed slug
        slug = 'admin'
        with self.assertRaises(ValidationError) as cm:
            block_slug_validator(slug)
        self.assertEqual(str(cm.exception.messages[0]), 'The slug cannot start with "admin".')

    def test_uppercase_slug(self):
        # Test an uppercase slug
        slug = 'TestSlug'
        with self.assertRaises(ValidationError) as cm:
            block_slug_validator(slug)
        self.assertEqual(str(cm.exception.messages[0]), 'Slugs must be lowercase.')

    def test_disallowed_prefix(self):
        # Test a disallowed prefix
        slug = 'admin-test'
        with self.assertRaises(ValidationError) as cm:
            block_slug_validator(slug)
        self.assertEqual(str(cm.exception.messages[0]), 'The slug cannot start with "admin".')

    def test_valid_prefix(self):
        # Test a valid prefix
        slug = 'test-admin'
        try:
            block_slug_validator(slug)
        except ValidationError:
            self.fail(f"Unexpected ValidationError raised for slug: {slug}")
