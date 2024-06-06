from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from .validators import validate_image_file

TARGET_CHOICES = (
    ('_self', 'Self'),
    ('_blank', 'Blank'),
    ('_parent', 'Parent'),
    ('_top', 'Top'),
)


class SVGAndImageFieldFile(ImageFieldFile):

    def save(self, name, content, save=True):

        if isinstance(content, UploadedFile) and (content.content_type == 'image/svg+xml' or name.endswith('.svg')):
            name = default_storage.save(name, content)
            self.name = name
            self._committed = True
        else:
            super().save(name, content, save)


class SVGAndImageField(models.ImageField):
    attr_class = SVGAndImageFieldFile


class Image(models.Model):
    file = SVGAndImageField(
        upload_to='%Y/%m/%d/',
        validators=[validate_image_file]
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    alt = models.CharField(max_length=255, blank=True, default='')
    href = models.URLField(blank=True, default='')
    rel = models.CharField(max_length=255, blank=True, default='')
    target = models.CharField(
        max_length=255,
        blank=True,
        choices=TARGET_CHOICES,
        default=TARGET_CHOICES[0]
    )
    tags = ArrayField(
        models.CharField(max_length=255), blank=True, default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or self.file.name or self.alt or 'Image'
