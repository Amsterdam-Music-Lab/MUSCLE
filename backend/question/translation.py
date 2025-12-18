from modeltranslation.translator import register, TranslationOptions
from .models import Choice, ChoiceList, Question


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'explainer')


@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('text',)

# register ChoiceList so we can display choices as TranslationTabularInline
@register(ChoiceList)
class ChoiceListTranslationOptions(TranslationOptions):
    fields = ()
