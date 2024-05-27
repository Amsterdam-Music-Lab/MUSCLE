from os.path import join

from django.conf import settings
from django.utils.translation import activate, gettext_lazy as _

from theme.models import FooterConfig, HeaderConfig, ThemeConfig


def serialize_footer(footer: FooterConfig) -> dict:
    return {
        'disclaimer': footer.disclaimer,
        'logos': [
            join(settings.MEDIA_URL, str(logo.file)) for logo in footer.logos.all()
        ],
        'privacy': footer.privacy
    }


def serialize_header(header: HeaderConfig) -> dict:
    return {
        'nextExperimentButtonText': _('Next experiment'),
        'aboutButtonText': _('About us'),
        'showScore': header.show_score
    }


def serialize_theme(theme: ThemeConfig) -> dict:
    return {
        'name': theme.name,
        'description': theme.description,
        'headingFontUrl': theme.heading_font_url,
        'bodyFontUrl': theme.body_font_url,
        'logoUrl': join(settings.MEDIA_URL, str(theme.logo_image.file)) if theme.logo_image else None,
        'backgroundUrl': join(settings.MEDIA_URL, str(theme.background_image.file)) if theme.background_image else None,
        'footer': serialize_footer(theme.footer) if hasattr(theme, 'footer') else None,
        'header': serialize_header(theme.header) if hasattr(theme, 'header') else None
    }
