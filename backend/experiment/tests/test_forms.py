from django.test import TestCase

from experiment.forms import BlockForm, BLOCK_RULES


class BlockFormTest(TestCase):
    def test_form_fields(self):
        form = BlockForm()
        self.assertIn("slug", form.fields)
        self.assertIn('rules', form.fields)
        self.assertIn('rounds', form.fields)
        self.assertIn('bonus_points', form.fields)
        self.assertIn('playlists', form.fields)

    def test_rules_field_choices(self):
        form = BlockForm()
        expected_choices = [(i, BLOCK_RULES[i].__name__) for i in BLOCK_RULES]
        expected_choices.append(("", "---------"))
        self.assertEqual(form.fields['rules'].choices, sorted(expected_choices))
