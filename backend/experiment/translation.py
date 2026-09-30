from modeltranslation.translator import register, TranslationOptions
from .models import Block, Experiment, Rank


@register(Block)
class BlockTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Experiment)
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


@register(Rank)
class RankTranslationOptions(TranslationOptions):
    fields = ('label', 'description', 'feedback')
