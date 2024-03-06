from django.contrib.postgres.fields import ArrayField
from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    alt = models.CharField(max_length=255)
    href = models.URLField()
    rel = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    tags = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)