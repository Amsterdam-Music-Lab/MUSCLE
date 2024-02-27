from django.db import models


class ThemeConfig(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Default')
    description = models.TextField(null=True, blank=True)
    font_url = models.CharField(null=True, blank=True, max_length=255)
    logo_url = models.CharField(null=True, blank=True, max_length=255)
    background_url = models.CharField(null=True, blank=True, max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

