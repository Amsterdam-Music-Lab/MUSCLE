from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.utils.html import format_html


from image.admin import ImageAdmin, TagsListFilter
from image.models import Image


class ImageAdminTest(TestCase):

    def setUp(self):
        self.admin = ImageAdmin(model=Image, admin_site=AdminSite())

    def test_image_preview_with_file(self):
        image = Image.objects.create(file='path/to/image.jpg')
        preview = self.admin.image_preview(image)
        expected_preview = format_html(
            '<img src="/upload/path/to/image.jpg" style="max-height: 50px;"/>')
        self.assertEqual(preview, expected_preview)

    def test_image_preview_without_file(self):
        image = Image.objects.create(file=None)
        preview = self.admin.image_preview(image)
        self.assertEqual(preview, "")

    def test_list_display(self):
        expected_list_display = ('image_preview', 'title', 'description', 'tags', 'created_at')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_search_fields(self):
        expected_search_fields = ['title', 'description', 'tags']
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_list_filter(self):
        expected_list_filter = [TagsListFilter]
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_fields(self):
        expected_fields = ['file', 'title', 'description', 'alt', 'href', 'rel', 'target', 'tags']
        self.assertEqual(self.admin.fields, expected_fields)

    def test_readonly_fields(self):
        expected_readonly_fields = ['created_at', 'updated_at']
        self.assertEqual(self.admin.readonly_fields, expected_readonly_fields)
