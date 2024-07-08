from modeltranslation.translator import register, TranslationOptions
from .models import ThemeConfig, FooterConfig


@register(ThemeConfig)
class ThemeConfigTranslationOptions(TranslationOptions):
    fields = ['description']


@register(FooterConfig)
class FooterConfigTranslationOptions(TranslationOptions):
    fields = ('disclaimer', 'privacy')
