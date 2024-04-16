from django.contrib.postgres.fields import ArrayField
from django.db import models

TARGET_CHOICES = (
    ('_self', 'Self'),
    ('_blank', 'Blank'),
    ('_parent', 'Parent'),
    ('_top', 'Top'),
)


class Image(models.Model):
    file = models.ImageField(upload_to='%Y/%m/%d/')
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
