from django.conf import settings
from django.test import TestCase

from image.models import Image
from theme.models import FooterConfig, HeaderConfig, ThemeConfig, SponsorImage
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
        third_image = Image.objects.create(
            file='thirdimage.jpg',
            href='https://third.example.com',
            alt='Third alt text',
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
        )
        # The order of the logos should be determined by the
        # index field in the through model and not by the order in
        # which they are added to the many-to-many field
        cls.footer.logos.add(logo_image, through_defaults={'index': 1})
        cls.footer.logos.add(background_image, through_defaults={'index': 0})
        cls.footer.logos.add(third_image, through_defaults={'index': 2})
        cls.header = HeaderConfig.objects.create(
            theme=cls.theme,
            show_score=True
        )

    def test_footer_serializer(self):
        expected_json = {
            'logos': [
                {
                    'file': f'{settings.BASE_URL}{settings.MEDIA_URL}anotherimage.png',
                    'href': 'https://other.example.com',
                    'alt': 'Another alt text',
                    'title': '',
                    'description': '',
                    'rel': '',
                    'tags': [],
                    'target': '',
                },
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
                    'file': f'{settings.BASE_URL}{settings.MEDIA_URL}thirdimage.jpg',
                    'href': 'https://third.example.com',
                    'alt': 'Third alt text',
                    'title': '',
                    'description': '',
                    'rel': '',
                    'tags': [],
                    'target': '',
                }
            ],
        }
        self.assertEqual(serialize_footer(self.footer), expected_json)

    def test_header_serializer(self):
        expected_json = {
            'nextBlockButtonText': 'Next experiment',
            'aboutButtonText': 'About us',
            'score': {
                'scoreClass': 'gold',
                'scoreLabel': 'Points',
                'noScoreLabel': 'No points yet!'
            }
        }
        self.assertEqual(serialize_header(self.header), expected_json)

    def default_colors(self):
        return {
            'colorPrimary': '#d843e2',
            'colorSecondary': '#39d7b8',
            'colorPositive': '#39d7b8',
            'colorNegative': '#fa5577',
            'colorNeutral1': '#ffb14c',
            'colorNeutral2': '#0cc7f1',
            'colorNeutral3': '#2b2bee',
            'colorGrey': '#bdbebf',
            'colorText': '#ffffff',
            'colorBackground': '#212529',
        }

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
            **self.default_colors(),
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
            **self.default_colors(),
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
            **self.default_colors(),
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
            **self.default_colors(),
            'backgroundUrl': f'{settings.BASE_URL}{settings.MEDIA_URL}anotherimage.png',
            'header': None,
            'footer': serialize_footer(self.footer),
        }
        self.assertEqual(serialize_theme(self.theme), expected_json)
