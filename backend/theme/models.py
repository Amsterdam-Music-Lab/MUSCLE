from django.db import models

from experiment.validators import markdown_html_validator


def footer_info_upload_path(instance, filename):
    """Generate path to save consent file based on experiment.slug"""
    folder_name = instance.slug
    return 'consent/{0}/{1}'.format(folder_name, filename)

class ThemeConfig(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Default')
    description = models.TextField(blank=True, default='')
    heading_font_url = models.CharField(blank=True, max_length=255, default='')
    body_font_url = models.CharField(blank=True, max_length=255, default='')
    logo_image = models.ForeignKey(
        'image.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='theme_logo')
    background_image = models.ForeignKey(
        'image.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='theme_background')

    def __str__(self):
        return self.name

    def __to_json__(self):
        return {
            'name': self.name,
            'description': self.description,
            'heading_font_url': self.heading_font_url,
            'body_font_url': self.body_font_url,
            'logo_image': self.logo_image.file,
            'background_image': self.background_image.file,
        }


class FooterConfig(models.Model):
    theme = models.OneToOneField(
        ThemeConfig, on_delete=models.CASCADE, related_name='footer')
    description = models.FileField(upload_to=footer_info_upload_path,
                                   blank=True,
                                   default='',
                                   help_text='Upload a file in html or markdown format',
                                   validators=[markdown_html_validator()])
    logos = models.ManyToManyField(
        to='image.Image', blank=True, help_text='Add references to Image objects; make sure these have sufficient contrast with the background (image).')
