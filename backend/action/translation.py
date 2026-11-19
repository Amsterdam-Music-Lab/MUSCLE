from modeltranslation.translator import register, TranslationOptions
from .models import Button, Explainer, FeedbackText, Final, Step


@register(Button)
class ButtonTranslationOptions(TranslationOptions):
    fields = ("label",)


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


@register(FeedbackText)
class FeedbackTextTranslationOptions(TranslationOptions):
    fields = ("text", "alternative_text")
