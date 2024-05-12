from django.test import TestCase
from image.models import Image


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Image.objects.create(
            file='path/to/image.jpg',
            title='Test Image',
            description='This is a test image',
            alt='Test Alt',
            href='https://example.com',
            rel='nofollow',
            target='_blank',
            tags=['tag1', 'tag2'],
        )

    def test_image_str(self):
        image = Image.objects.get(title='Test Image')
        self.assertEqual(str(image), 'Test Image')

    def test_image_fields(self):
        image = Image.objects.get(title='Test Image')
        self.assertEqual(image.file, 'path/to/image.jpg')
        self.assertEqual(image.title, 'Test Image')
        self.assertEqual(image.description, 'This is a test image')
        self.assertEqual(image.alt, 'Test Alt')
        self.assertEqual(image.href, 'https://example.com')
        self.assertEqual(image.rel, 'nofollow')
        self.assertEqual(image.target, '_blank')
        self.assertEqual(image.tags, ['tag1', 'tag2'])