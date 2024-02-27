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

    def __dict__(self):
        return {
            'name': self.name,
            'description': self.description,
            'font_url': self.font_url,
            'logo_url': self.logo_url,
            'background_url': self.background_url,
            'active': self.active
        }