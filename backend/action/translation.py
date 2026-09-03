from modeltranslation.translator import register, TranslationOptions
from .models import Explainer, Final, FinalFeedback, FinalScore, Rank, Step

@register(Explainer)
class ExplainerTranslationOptions(TranslationOptions):
    fields = ("instruction",)


# register Final model so we can display choices as TranslationTabularInline
@register(Final)
class FinalTranslationOptions(TranslationOptions):
    fields = ()


@register(FinalFeedback)
class FinalFeedbackTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(FinalScore)
class FinalScoreTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Rank)
class RankTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ("description",)
