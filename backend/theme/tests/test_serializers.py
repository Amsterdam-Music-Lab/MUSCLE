from django.conf import settings
from django.test import TestCase

from image.models import Image
from theme.models import FooterConfig, HeaderConfig, ThemeConfig
from theme.serializers import serialize_footer, serialize_header, serialize_theme


class ThemeConfigSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logo_image = Image.objects.create(
            file='someimage.jpg'
        )
        background_image = Image.objects.create(
            file='anotherimage.png'
        )
        cls.theme = ThemeConfig.objects.create(
            name='Default',
            description='Default theme configuration',
            heading_font_url='https://example.com/heading_font',
            body_font_url='https://example.com/body_font',
            logo_image=logo_image,
            background_image=background_image,
        )
        cls.footer = FooterConfig.objects.create(
            theme=cls.theme,
            disclaimer='Some [more information][https://example.com/our-team]'
        )
        cls.footer.logos.add(logo_image)
        cls.footer.logos.add(background_image)
        cls.header = HeaderConfig.objects.create(
            theme=cls.theme,
            show_score=True
        )

    def test_footer_serializer(self):
        expected_json = {
            'disclaimer': 'Some [more information][https://example.com/our-team]',
            'logos': [f'{settings.MEDIA_URL}someimage.jpg', f'{settings.MEDIA_URL}anotherimage.png'],
            'privacy': ''
        }
        self.assertEqual(serialize_footer(self.footer), expected_json)

    def test_header_serializer(self):
        expected_json = {
            'showScore': True,
            'nextExperimentButtonText': 'Next experiment',
            'aboutButtonText': 'About us'
        }
        self.assertEqual(serialize_header(self.header), expected_json)

    def test_theme_config_serializer(self):
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'headingFontUrl': 'https://example.com/heading_font',
            'bodyFontUrl': 'https://example.com/body_font',
            'logoUrl': f'{settings.MEDIA_URL}someimage.jpg',
            'backgroundUrl': f'{settings.MEDIA_URL}anotherimage.png',
            'footer': serialize_footer(self.footer),
            'header': serialize_header(self.header),
        }
        self.assertEqual(serialize_theme(self.theme), expected_json)

    def test_theme_serialization_no_image(self):
        theme_config = self.theme
        theme_config.background_image = None
        theme_config.logo_image = None
        theme_config.save()
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'headingFontUrl': 'https://example.com/heading_font',
            'bodyFontUrl': 'https://example.com/body_font',
            'logoUrl': None,
            'backgroundUrl': None,
            'footer': serialize_footer(self.footer),
            'header': serialize_header(self.header),
        }
        self.assertEqual(serialize_theme(theme_config), expected_json)

    def test_theme_serialization_no_footer(self):
        self.theme.footer = None
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'headingFontUrl': 'https://example.com/heading_font',
            'bodyFontUrl': 'https://example.com/body_font',
            'logoUrl': f'{settings.MEDIA_URL}someimage.jpg',
            'backgroundUrl': f'{settings.MEDIA_URL}anotherimage.png',
            'header': serialize_header(self.header),
            'footer': None,
        }
        self.assertEqual(serialize_theme(self.theme), expected_json)

    def test_theme_serialization_no_header(self):
        self.theme.header = None
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'headingFontUrl': 'https://example.com/heading_font',
            'bodyFontUrl': 'https://example.com/body_font',
            'logoUrl': f'{settings.MEDIA_URL}someimage.jpg',
            'backgroundUrl': f'{settings.MEDIA_URL}anotherimage.png',
            'header': None,
            'footer': serialize_footer(self.footer),
        }
        self.assertEqual(serialize_theme(self.theme), expected_json)
