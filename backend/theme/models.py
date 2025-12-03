from django.db import models

from experiment.actions.utils import camelize

class ThemeConfig(models.Model):
    """A model defining the theme of an experiment or block

    Attributes:
        name (str): The name of this theme configuration
        description (str): The description of this theme config
        heading_font_url (str): Url of the heading font
        body_font_url (str): Url of the body font
        logo_image (image.models.Image): Linked image to be used as logo
        background_image (image.models.Image): Linked image to be used as background
    """
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

    color_primary = models.CharField(max_length=255, blank=True, default='#d843e2')
    color_secondary = models.CharField(max_length=255, blank=True, default='#39d7b8')
    color_positive = models.CharField(max_length=255, blank=True, default='#00b612')
    color_negative = models.CharField(max_length=255, blank=True, default='#fa5577')
    color_neutral1 = models.CharField(max_length=255, blank=True, default='#ffb14c')
    color_neutral2 = models.CharField(max_length=255, blank=True, default='#0cc7f1')
    color_neutral3 = models.CharField(max_length=255, blank=True, default='#2b2bee')
    color_grey = models.CharField(max_length=255, blank=True, default='#bdbebf')
    color_text = models.CharField(max_length=255, blank=True, default='#ffffff')
    color_background = models.CharField(max_length=255, blank=True, default='#212529')

    def __str__(self):
        return self.name

    def valid_colors(self):
        return [
            camelize(color)
            for color in filter(lambda x: x.startswith('color'), dir(self))
        ]


class SponsorImage(models.Model):
    """A model to define sponsor images for the footer configuration

    Attributes:
        footer_config (FooterConfig): Linked footer configuration
        image (image.models.Image): Linked image to be used as sponsor image
        index (int): Order in which the image should be displayed
    """
    footer_config = models.ForeignKey('FooterConfig', on_delete=models.CASCADE, related_name='sponsor_images')
    image = models.ForeignKey('image.Image', on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    class Meta:
        ordering = ['index']
        unique_together = [['footer_config', 'image']]

    def __str__(self):
        return f"{self.image.title} (Sponsor {self.index + 1})"


class FooterConfig(models.Model):
    """A model defining the configuration of the footer

    Attributes:
        theme (ThemeConfig): Linked theme configuration
        logos (SponsorImage): Linked sponsor images
    """
    theme = models.OneToOneField(
        'ThemeConfig', on_delete=models.CASCADE, related_name='footer')
    logos = models.ManyToManyField(
        to='image.Image',
        through='SponsorImage',
        related_name='footer_configs',
        blank=True,
        help_text='Add references to Image objects; make sure these have sufficient contrast with the background (image).'
    )

    def __str__(self):
        return f"Footer for {self.theme.name}"


class HeaderConfig(models.Model):
    """A model defing the header configuration

    Attributes:
        theme (ThemeConfig): Linked theme configuration
        show_score (bool): Should the score be shown in the header?
    """
    theme = models.OneToOneField(
        ThemeConfig, on_delete=models.CASCADE, related_name='header')
    show_score = models.BooleanField(default=False)
