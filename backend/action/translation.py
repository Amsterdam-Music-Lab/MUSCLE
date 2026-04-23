from modeltranslation.translator import register, TranslationOptions
from .models import Button, Explainer, Step


@register(Button)
class ExplainerTranslationOptions(TranslationOptions):
    fields = ('label', )


@register(Explainer)
class ExplainerTranslationOptions(TranslationOptions):
    fields = ('instruction', )


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('description', )