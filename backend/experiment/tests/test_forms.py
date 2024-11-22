from django.test import TestCase

from experiment.forms import BlockForm, ExportForm, TemplateForm, BLOCK_RULES, SESSION_CHOICES, RESULT_CHOICES, EXPORT_OPTIONS, TEMPLATE_CHOICES


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


class ExportFormTest(TestCase):
    def test_form_fields(self):
        form = ExportForm()
        self.assertIn('export_session_fields', form.fields)
        self.assertIn('export_result_fields', form.fields)
        self.assertIn('export_options', form.fields)

    def test_field_choices(self):
        form = ExportForm()
        self.assertEqual(form.fields['export_session_fields'].choices, SESSION_CHOICES)
        self.assertEqual(form.fields['export_result_fields'].choices, RESULT_CHOICES)
        self.assertEqual(form.fields['export_options'].choices, EXPORT_OPTIONS)


class TemplateFormTest(TestCase):
    def test_form_fields(self):
        form = TemplateForm()
        self.assertIn('select_template', form.fields)

    def test_template_choices(self):
        form = TemplateForm()
        self.assertEqual(form.fields['select_template'].choices, TEMPLATE_CHOICES)
