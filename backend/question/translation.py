from modeltranslation.translator import register, TranslationOptions
from .models import Question, Choice


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'explainer')


@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('text',)
