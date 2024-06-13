from django.conf import settings
from django.test import TestCase

from image.models import Image
from theme.models import FooterConfig, HeaderConfig, ThemeConfig
from theme.serializers import serialize_footer, serialize_header, serialize_theme


class ThemeConfigSerializerTest(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        logo_image = Image.objects.create(
            title='Image',
            description='',
            file='someimage.jpg',
            href='https://example.com',
            alt='Alt text',
            target='_self',
            rel='',
        )
        background_image = Image.objects.create(
            file='anotherimage.png',
            href='https://other.example.com',
            alt='Another alt text',
            target='',
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
            disclaimer='Some [information](https://example.com/our-team)',
            privacy='Some privacy message'
        )
        cls.footer.logos.add(logo_image)
        cls.footer.logos.add(background_image)
        cls.header = HeaderConfig.objects.create(
            theme=cls.theme,
            show_score=True
        )

    def test_footer_serializer(self):
        expected_json = {
            'disclaimer': '<p>Some <a href="https://example.com/our-team">information</a></p>',
            'logos': [
                {
                    'file': f'{settings.BASE_URL}{settings.MEDIA_URL}someimage.jpg',
                    'href': 'https://example.com',
                    'alt': 'Alt text',
                    'title': 'Image',
                    'description': '',
                    'rel': '',
                    'target': '_self',
                    'tags': [],
                },
                {
                    'file': f'{settings.BASE_URL}{settings.MEDIA_URL}anotherimage.png',
                    'href': 'https://other.example.com',
                    'alt': 'Another alt text',
                    'title': '',
                    'description': '',
                    'rel': '',
                    'tags': [],
                    'target': '',
                }
            ],
            'privacy': '<p>Some privacy message</p>'
        }
        self.assertEqual(serialize_footer(self.footer), expected_json)

    def test_header_serializer(self):
        expected_json = {            
            'nextExperimentButtonText': 'Next experiment',
            'aboutButtonText': 'About us',
            'score': {
                'scoreClass': 'gold',
                'scoreLabel': 'Points',
                'noScoreLabel': 'No points yet!'
            }
        }
        self.assertEqual(serialize_header(self.header), expected_json)

    def test_theme_config_serializer(self):
        expected_json = {
            'name': 'Default',
            'description': 'Default theme configuration',
            'headingFontUrl': 'https://example.com/heading_font',
            'bodyFontUrl': 'https://example.com/body_font',
            'logo': {
                'file': f'{settings.BASE_URL}{settings.MEDIA_URL}someimage.jpg',
                'href': 'https://example.com',
                'alt': 'Alt text',
                'title': 'Image',
                'description': '',
                'rel': '',
                'tags': [],
                'target': '_self',
            },
            'backgroundUrl': f'{settings.BASE_URL}{settings.MEDIA_URL}anotherimage.png',
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
            'logo': None,
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
            'logo': {
                'file': f'{settings.BASE_URL}{settings.MEDIA_URL}someimage.jpg',
                'href': 'https://example.com',
                'alt': 'Alt text',
                'title': 'Image',
                'description': '',
                'rel': '',
                'target': '_self',
                'tags': [],
            },
            'backgroundUrl': f'{settings.BASE_URL}{settings.MEDIA_URL}anotherimage.png',
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
            'logo': {
                'file': f'{settings.BASE_URL}{settings.MEDIA_URL}someimage.jpg',
                'href': 'https://example.com',
                'alt': 'Alt text',
                'title': 'Image',
                'description': '',
                'rel': '',
                'target': '_self',
                'tags': [],
            },
            'backgroundUrl': f'{settings.BASE_URL}{settings.MEDIA_URL}anotherimage.png',
            'header': None,
            'footer': serialize_footer(self.footer),
        }
        self.assertEqual(serialize_theme(self.theme), expected_json)
