from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.utils.safestring import mark_safe

from image.admin import ImageAdmin
from image.models import Image


class ImageAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.site = AdminSite()
        cls.admin = ImageAdmin(Image, cls.site)

    def test_image_preview_with_file_url(self):
        image = Image.objects.create(file='path/to/image.jpg')
        request = self.factory.get('/')
        preview = self.admin.image_preview(image)
        expected_preview = mark_safe('<img src="path/to/image.jpg" style="max-height: 50px;"/>')
        self.assertEqual(preview, expected_preview)

    def test_image_preview_without_file_url(self):
        image = Image.objects.create(file=None)
        request = self.factory.get('/')
        preview = self.admin.image_preview(image)
        self.assertEqual(preview, "")

    def test_list_display(self):
        expected_list_display = ('image_preview', 'title', 'description', 'tags', 'created_at')
        self.assertEqual(self.admin.list_display, expected_list_display)

    def test_search_fields(self):
        expected_search_fields = ['title', 'description', 'tags']
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_list_filter(self):
        expected_list_filter = ['TagsListFilter']
        self.assertEqual(self.admin.list_filter, expected_list_filter)

    def test_fields(self):
        expected_fields = ['file', 'title', 'description', 'alt', 'href', 'rel', 'target', 'tags']
        self.assertEqual(self.admin.fields, expected_fields)

    def test_readonly_fields(self):
        expected_readonly_fields = ['created_at', 'updated_at']
        self.assertEqual(self.admin.readonly_fields, expected_readonly_fields)

    def test_experiment_link(self):
        experiment = Experiment.objects.create(name="Test Experiment")
        request = self.factory.get('/')
        link = self.admin.experiment_link(experiment)
        expected_url = reverse("admin:experiment_experiment_change", args=[experiment.pk])
        expected_name = "Test Experiment"
        expected_link = format_html('<a href="{}">{}</a>', expected_url, expected_name)
        self.assertEqual(link, expected_link)