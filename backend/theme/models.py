from django.db import models

class ThemeConfig(models.Model):
    css_variables = models.TextField()  # Store all hard-coded variables as text
    additional_variables = models.TextField(blank=True)
    global_css = models.TextField(blank=True)
