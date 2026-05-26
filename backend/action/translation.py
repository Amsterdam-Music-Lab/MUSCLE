from modeltranslation.translator import register, TranslationOptions
from .models import Explainer, Step

@register(Explainer)
class ExplainerTranslationOptions(TranslationOptions):
    fields = ('instruction', )


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('description', )
