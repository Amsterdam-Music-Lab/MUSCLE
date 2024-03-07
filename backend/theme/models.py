from django.db import models


class ThemeConfig(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Default')
    description = models.TextField(null=True, blank=True)
    heading_font_url = models.CharField(null=True, blank=True, max_length=255)
    body_font_url = models.CharField(null=True, blank=True, max_length=255)
    logo_url = models.CharField(null=True, blank=True, max_length=255)
    background_url = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def __to_json__(self):
        return {
            'name': self.name,
            'description': self.description,
            'heading_font_url': self.heading_font_url,
            'body_font_url': self.body_font_url,
            'logo_url': self.logo_url,
            'background_url': self.background_url,
        }
