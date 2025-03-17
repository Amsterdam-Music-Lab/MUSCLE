from modeltranslation.translator import register, TranslationOptions
from .models import BlockTranslatedContent, ExperimentTranslatedContent


@register(BlockTranslatedContent)
class BlockTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(ExperimentTranslatedContent)
class ExperimentTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'consent', 'about_content', 'social_media_message', 'disclaimer', 'privacy')

