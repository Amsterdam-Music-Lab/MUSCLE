from django.contrib.postgres.fields import ArrayField
from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    href = models.URLField(blank=True, null=True)
    rel = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    tags = ArrayField(
        models.CharField(max_length=255), blank=True, default=list, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
