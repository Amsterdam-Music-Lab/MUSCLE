from django.test import TestCase

from image.models import Image
from theme.models import FooterConfig, ThemeConfig


class ThemeConfigModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logo_image = Image.objects.create(
            file='someimage.jpg'
        )
        background_image = Image.objects.create(
            file='anotherimage.png'
        )
        theme = ThemeConfig.objects.create(
            name='Default',
            description='Default theme configuration',
            heading_font_url='https://example.com/heading_font',
            body_font_url='https://example.com/body_font',
            logo_image=logo_image,
            background_image=background_image,
        )
        cls.footer = FooterConfig.objects.create(
            theme=theme,
            disclaimer='Some [more information][https://example.com/our-team]'
        )

    def test_theme_config_str(self):
        theme_config = ThemeConfig.objects.get(name='Default')
        self.assertEqual(str(theme_config), 'Default')

    def test_footer_to_json(self):
        expected_json = {
            'disclaimer': 'Some [more information][https://example.com/our-team]',
            'logos': [],
            'privacy': ''
        }
        self.assertEqual(self.footer.to_json(), expected_json)

    def test_theme_config_to_json(self):
        theme_config = ThemeConfig.objects.get(name='Default')
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'heading_font_url': 'https://example.com/heading_font',
            'body_font_url': 'https://example.com/body_font',
            'logo_image': 'someimage.jpg',
            'background_image': 'anotherimage.png',
            'footer': self.footer.to_json(),
        }
        self.assertEqual(theme_config.to_json(), expected_json)

    def test_theme_serialization_no_image(self):
        theme_config = ThemeConfig.objects.get(name='Default')
        theme_config.background_image = None
        theme_config.logo_image = None
        theme_config.save()
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'heading_font_url': 'https://example.com/heading_font',
            'body_font_url': 'https://example.com/body_font',
            'logo_image': None,
            'background_image': None,
            'footer': self.footer.to_json()
        }
        self.assertEqual(theme_config.to_json(), expected_json)

    def test_theme_serialization_no_footer(self):
        theme_config = ThemeConfig.objects.get(name='Default')
        self.footer.delete()
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'heading_font_url': 'https://example.com/heading_font',
            'body_font_url': 'https://example.com/body_font',
            'logo_image': 'someimage.jpg',
            'background_image': 'anotherimage.png',
            'footer': None,
        }
        self.assertEqual(theme_config.to_json(), expected_json)
