from modeltranslation.translator import register, TranslationOptions
from .models import Explainer, Final, Step

@register(Explainer)
class ExplainerTranslationOptions(TranslationOptions):
    fields = ("instruction",)


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(Final)
class FinalTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "score_label",
    )
