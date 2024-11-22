from modeltranslation.translator import register, TranslationOptions
from .models import Question, Choice


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', 'explainer')


@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('text',)

