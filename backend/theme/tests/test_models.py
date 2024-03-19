from django.test import TestCase

from image.models import Image
from theme.models import ThemeConfig


class ThemeConfigModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logo_image = Image.objects.create(
            file='someimage.jpg'
        )
        background_image = Image.objects.create(
            file='anotherimage.png'
        )
        ThemeConfig.objects.create(
            name='Default',
            description='Default theme configuration',
            heading_font_url='https://example.com/heading_font',
            body_font_url='https://example.com/body_font',
            logo_image=logo_image,
            background_image=background_image,
        )

    def test_theme_config_str(self):
        theme_config = ThemeConfig.objects.get(name='Default')
        self.assertEqual(str(theme_config), 'Default')

    def test_theme_config_to_json(self):
        theme_config = ThemeConfig.objects.get(name='Default')
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'heading_font_url': 'https://example.com/heading_font',
            'body_font_url': 'https://example.com/body_font',
            'logo_image': 'someimage.jpg',
            'background_image': 'anotherimage.png',
        }
        self.assertEqual(theme_config.__to_json__(), expected_json)
