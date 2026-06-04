from django.core.exceptions import ValidationError
from django.test import TestCase

from experiment.validators import identifier_validator

class ExperimentValidatorsTest(TestCase):

    def test_valid_identifier(self):
        # Test a valid lowercase identifier
        identifier = 'testidentifier'
        try:
            identifier_validator(identifier)
        except ValidationError:
            self.fail(f"Unexpected ValidationError raised for identifier: {identifier}")

    def test_disallowed_identifier(self):
        # Test a disallowed identifier
        identifier = 'admin'
        with self.assertRaises(ValidationError) as cm:
            identifier_validator(identifier)
        self.assertEqual(
            str(cm.exception.messages[0]), 'The identifier cannot start with "admin".'
        )

    def test_uppercase_identifier(self):
        # Test an uppercase identifier
        identifier = 'TestIdentifier'
        with self.assertRaises(ValidationError) as cm:
            identifier_validator(identifier)
        self.assertEqual(
            str(cm.exception.messages[0]), 'Identifiers must be lowercase.'
        )

    def test_disallowed_prefix(self):
        # Test a disallowed prefix
        identifier = 'admin-test'
        with self.assertRaises(ValidationError) as cm:
            identifier_validator(identifier)
        self.assertEqual(
            str(cm.exception.messages[0]), 'The identifier cannot start with "admin".'
        )

    def test_valid_prefix(self):
        # Test a valid prefix
        identifier = 'test-admin'
        try:
            identifier_validator(identifier)
        except ValidationError:
            self.fail(f"Unexpected ValidationError raised for identifier: {identifier}")
