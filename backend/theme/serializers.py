from os.path import join

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_markup.markup import formatter

from image.serializers import serialize_image
from theme.models import FooterConfig, HeaderConfig, ThemeConfig


def serialize_footer(footer: FooterConfig) -> dict:
    return {
        'logos': [
            serialize_image(logo)
            for logo in footer.logos.all().order_by('sponsorimage__index')
        ],
    }


def serialize_header(header: HeaderConfig) -> dict:
    return {
        'nextBlockButtonText': _('Next experiment'),
        'aboutButtonText': _('About us'),
        'score': {
            'scoreClass': 'gold',
            'scoreLabel': _('Points'),
            'noScoreLabel': _('No points yet!')
            } if header.show_score else None,
    }


def serialize_theme(theme: ThemeConfig) -> dict:
    return {
        'name': theme.name,
        'description': theme.description,
        'headingFontUrl': theme.heading_font_url,
        'bodyFontUrl': theme.body_font_url,
        'logo': serialize_image(theme.logo_image) if theme.logo_image else None,
        'backgroundUrl': (
            f'{settings.BASE_URL.strip("/")}/{settings.MEDIA_URL.strip("/")}/{str(theme.background_image.file)}'
            if theme.background_image
            else None
        ),
        'footer': serialize_footer(theme.footer) if hasattr(theme, 'footer') else None,
        'header': serialize_header(theme.header) if hasattr(theme, 'header') else None,
        'colorPrimary': theme.color_primary,
        'colorSecondary': theme.color_secondary,
        'colorPositive': theme.color_positive,
        'colorNegative': theme.color_negative,
        'colorNeutral1': theme.color_neutral1,
        'colorNeutral2': theme.color_neutral2,
        'colorNeutral3': theme.color_neutral3,
        'colorGrey': theme.color_grey,
        'colorText': theme.color_text,
        'colorBackground': theme.color_background,
    }
