from django.db import models


class ThemeConfig(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Default')
    description = models.TextField(blank=True, default='')
    heading_font_url = models.CharField(blank=True, max_length=255, default='')
    body_font_url = models.CharField(blank=True, max_length=255, default='')
    logo_image = models.ForeignKey(
        'image.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='theme_logo')
    background_image = models.ForeignKey(
        'image.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='theme_background')

    def __str__(self):
        return self.name


class SponsorImage(models.Model):
    footer_config = models.ForeignKey('FooterConfig', on_delete=models.CASCADE, related_name='sponsor_images')
    image = models.ForeignKey('image.Image', on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    class Meta:
        ordering = ['index']
        unique_together = [['footer_config', 'image']]

    def __str__(self):
        return f"{self.image.title} (Sponsor {self.index + 1})"


class FooterConfig(models.Model):
    theme = models.OneToOneField(
        'ThemeConfig', on_delete=models.CASCADE, related_name='footer')
    disclaimer = models.TextField(blank=True, default='')
    logos = models.ManyToManyField(
        to='image.Image',
        through='SponsorImage',
        related_name='footer_configs',
        blank=True,
        help_text='Add references to Image objects; make sure these have sufficient contrast with the background (image).'
    )
    privacy = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Footer for {self.theme.name}"


class HeaderConfig(models.Model):
    theme = models.OneToOneField(
        ThemeConfig, on_delete=models.CASCADE, related_name='header')
    show_score = models.BooleanField(default=False)
