from django.db import models


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

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'heading_font_url': self.heading_font_url,
            'body_font_url': self.body_font_url,
            'logo_image': str(self.logo_image.file) if self.logo_image else None,
            'background_image': str(self.background_image.file) if self.background_image else None,
            'footer': self.footer.to_json() if hasattr(self, 'footer') else None
        }


class FooterConfig(models.Model):
    theme = models.OneToOneField(
        ThemeConfig, on_delete=models.CASCADE, related_name='footer')
    disclaimer = models.TextField(blank=True, default='')
    logos = models.ManyToManyField(
        to='image.Image', blank=True, help_text='Add references to Image objects; make sure these have sufficient contrast with the background (image).')
    privacy = models.TextField(blank=True, default='')

    def to_json(self):
        return {
            'disclaimer': self.disclaimer,
            'logos': [
                str(logo.file) for logo in self.logos.all()
            ],
            'privacy': self.privacy
        }
