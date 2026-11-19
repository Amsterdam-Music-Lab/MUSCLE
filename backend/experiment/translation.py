from modeltranslation.translator import register, TranslationOptions
from .models import Block, Experiment, Rank, Ranking, Reward

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


@register(Ranking)
class RankingTranslationOptions(TranslationOptions):
    fields = ()


@register(Rank)
class RankTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Reward)
class RewardTranslationOptions(TranslationOptions):
    fields = ('text',)
