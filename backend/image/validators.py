import os
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator(object):

    def __init__(self, allowed_extensions=None, allowed_mimetypes=None):
        self.allowed_extensions = allowed_extensions
        self.allowed_mimetypes = allowed_mimetypes

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1].lower()

        print('Antoinette!', value, ext)

        if self.allowed_extensions and ext not in self.allowed_extensions:
            raise ValidationError(f'Unsupported file extension: {ext}.')


validate_image_file = FileValidator(
    allowed_extensions=['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',],
    allowed_mimetypes=[
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/svg+xml',
        'image/webp',
    ]
)
