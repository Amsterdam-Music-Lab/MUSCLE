from django.db import models


class AdminInterfaceConfiguration(models.Model):
    """Model for storing the configuration of the admin interface"""
    name = models.CharField(max_length=255, unique=True, default='Default')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
        }


class AdminInterfaceThemeConfiguration(models.Model):
    """Model for storing the theme configuration of the admin interface"""
    configuration = models.OneToOneField(
        AdminInterfaceConfiguration, on_delete=models.CASCADE, related_name='theme')

    # Color scheme
    color_default_bg = models.CharField(max_length=255, blank=True, default='#f8d7da')
    color_default_fg = models.CharField(max_length=255, blank=True, default='#721c24')
    color_success_bg = models.CharField(max_length=255, blank=True, default='#d4edda')
    color_success_fg = models.CharField(max_length=255, blank=True, default='#155724')
    color_warning_bg = models.CharField(max_length=255, blank=True, default='#fff3cd')
    color_warning_fg = models.CharField(max_length=255, blank=True, default='#856404')
    color_error_bg = models.CharField(max_length=255, blank=True, default='#f8d7da')
    color_error_fg = models.CharField(max_length=255, blank=True, default='#721c24')
