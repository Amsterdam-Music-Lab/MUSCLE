from modeltranslation.translator import register, TranslationOptions
from .models import BlockText, ExperimentText


@register(BlockText)
class BlockTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(ExperimentText)
class ExperimentTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'consent',
        'about_content',
        'social_media_message',
        'disclaimer',
        'privacy',
    )
