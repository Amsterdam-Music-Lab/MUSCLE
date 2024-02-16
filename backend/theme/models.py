from django.db import models


class ThemeConfig(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Default')
    font = models.CharField(null=True, blank=True, max_length=255)
    logo = models.CharField(null=True, blank=True, max_length=255)
    background = models.CharField(null=True, blank=True, max_length=255)
    css_variables = models.TextField()  # Store all hard-coded variables as text
    additional_variables = models.TextField(null=True, blank=True)
    global_css = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
