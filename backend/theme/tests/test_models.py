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
        theme = ThemeConfig.objects.create(
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
