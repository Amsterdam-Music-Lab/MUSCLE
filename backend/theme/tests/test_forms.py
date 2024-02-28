from django.test import TestCase

from theme.forms import ThemeConfigForm
from theme.models import ThemeConfig


class ThemeConfigFormTest(TestCase):
    def test_form_fields(self):
        form = ThemeConfigForm()
        self.assertEqual(form.Meta.model, ThemeConfig)
        self.assertEqual(form.Meta.fields, '__all__')

    def test_form_media(self):
        form = ThemeConfigForm()
        self.assertEqual(form.Media.js, ['img_preview.js', 'font_preview.js'])

    def test_save_method(self):
        form = ThemeConfigForm()
        instance = form.save(commit=False)
        self.assertIsInstance(instance, ThemeConfig)
        self.assertFalse(instance.pk)

        instance.save()
        self.assertTrue(instance.pk)
