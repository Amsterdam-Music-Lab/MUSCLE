from django.test import TestCase

from experiment.forms import BlockForm, BLOCK_RULES
from experiment.models import Block, Experiment, Phase

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

    def test_clean_slug(self):
        experiment = Experiment.objects.create(slug="test")
        phase = Phase.objects.create(experiment=experiment)

        Block.objects.create(phase=phase, slug="test1")
        block2 = Block.objects.create(phase=phase)

        form_data = {
            "slug": "test1",
            "name": "Test Block",
            "index": 1,
            "rules": "QUESTIONNAIRE",
            "rounds": 1,
            "bonus_points": 0,
        }
        form = BlockForm(form_data, instance=block2)
        self.assertFalse(form.is_valid())
        self.assertIn("slug", form.errors.keys())
        self.assertIn("not unique", form.errors.get("slug")[0])
