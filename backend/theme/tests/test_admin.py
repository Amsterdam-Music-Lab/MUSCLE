from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

from theme.admin import ThemeConfigAdmin
from theme.models import ThemeConfig


class ThemeConfigAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.site = AdminSite()
        cls.admin = ThemeConfigAdmin(ThemeConfig, cls.site)

    def test_name_link(self):
        theme = ThemeConfig.objects.create(name='Test Theme')
        request = self.factory.get('/')
        link = self.admin.name_link(theme)
        expected_link = f'<a href="/admin/theme/themeconfig/{theme.id}/change/">{theme.name}</a>'
        self.assertEqual(link, expected_link)

    def test_heading_font_preview_with_url(self):
        theme = ThemeConfig.objects.create(heading_font_url='https://example.com/font.css')
        request = self.factory.get('/')
        preview = self.admin.heading_font_preview(theme)
        expected_preview = (
            '<link href="https://example.com/font.css" rel="stylesheet">'
            '<div style="font-family: \'sans-serif\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_heading_font_preview_with_google_font_name(self):
        theme = ThemeConfig.objects.create(heading_font_url='Roboto')
        request = self.factory.get('/')
        preview = self.admin.heading_font_preview(theme)
        expected_preview = (
            '<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">'
            '<div style="font-family: \'Roboto\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_heading_font_preview_with_no_font(self):
        theme = ThemeConfig.objects.create(heading_font_url=None)
        request = self.factory.get('/')
        preview = self.admin.heading_font_preview(theme)
        self.assertEqual(preview, "No font selected")

    def test_body_font_preview_with_url(self):
        theme = ThemeConfig.objects.create(body_font_url='https://example.com/font.css')
        request = self.factory.get('/')
        preview = self.admin.body_font_preview(theme)
        expected_preview = (
            '<link href="https://example.com/font.css" rel="stylesheet">'
            '<div style="font-family: \'sans-serif\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_body_font_preview_with_google_font_name(self):
        theme = ThemeConfig.objects.create(body_font_url='Roboto')
        request = self.factory.get('/')
        preview = self.admin.body_font_preview(theme)
        expected_preview = (
            '<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">'
            '<div style="font-family: \'Roboto\'; font-size: 16px;">Preview Text</div>'
        )
        self.assertEqual(preview, expected_preview)

    def test_body_font_preview_with_no_font(self):
        theme = ThemeConfig.objects.create(body_font_url=None)
        request = self.factory.get('/')
        preview = self.admin.body_font_preview(theme)
        self.assertEqual(preview, "No font selected")
