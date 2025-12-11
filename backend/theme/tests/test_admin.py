from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from image.models import Image
from theme.admin import ThemeConfigAdmin
from theme.models import FooterConfig, ThemeConfig


class ThemeConfigAdminTest(TestCase):

    def setUp(self):
        self.admin = ThemeConfigAdmin(model=ThemeConfig, admin_site=AdminSite())

    def test_heading_font_preview_with_url(self):
        theme = ThemeConfig.objects.create(heading_font_url='https://example.com/font.css')
        preview = self.admin.heading_font_preview(theme)
        expected_preview = (
            '<link href="https://example.com/font.css" rel="stylesheet">'
            '<div style="font-family: \'sans-serif\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_heading_font_preview_with_google_font_name(self):
        theme = ThemeConfig.objects.create(heading_font_url='Roboto')
        preview = self.admin.heading_font_preview(theme)
        expected_preview = (
            '<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">'
            '<div style="font-family: \'Roboto\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_heading_font_preview_with_no_font(self):
        theme = ThemeConfig.objects.create(heading_font_url='')
        preview = self.admin.heading_font_preview(theme)
        self.assertEqual(preview, "No font selected")

    def test_body_font_preview_with_url(self):
        theme = ThemeConfig.objects.create(body_font_url='https://example.com/font.css')
        preview = self.admin.body_font_preview(theme)
        expected_preview = (
            '<link href="https://example.com/font.css" rel="stylesheet">'
            '<div style="font-family: \'sans-serif\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_body_font_preview_with_google_font_name(self):
        theme = ThemeConfig.objects.create(body_font_url='Roboto')
        preview = self.admin.body_font_preview(theme)
        expected_preview = (
            '<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">'
            '<div style="font-family: \'Roboto\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_body_font_preview_with_no_font(self):
        theme = ThemeConfig.objects.create(body_font_url='')
        preview = self.admin.body_font_preview(theme)
        self.assertEqual(preview, "No font selected")

    def test_footer_overview(self):
        theme = ThemeConfig.objects.create(name='MyTheme')
        footer = FooterConfig.objects.create(theme=theme)
        footer.logos.add(
            Image.objects.create(file='path/to/image.jpg'),
            through_defaults={'index': 1}
        )
        footer.logos.add(
            Image.objects.create(file='path/to/another/image.png'),
            through_defaults={'index': 0}
        )
        preview = self.admin.footer_overview(theme)
        self.assertEqual(preview, "Footer with 2 logos")
