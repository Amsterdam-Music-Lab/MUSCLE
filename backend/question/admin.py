from copy import deepcopy
import logging

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from question.models import (
    Choice,
    ChoiceList,
    Question,
    QuestionList,
    QuestionInList,
)
from question.forms import QuestionForm, QuestionListForm
from result.models import Result
from result.utils import apply_scoring_rule

logger = logging.getLogger(__name__)

class QuestionInListInline(admin.TabularInline):
    model = QuestionInList
    extra = 0


class QuestionListInline(admin.TabularInline):
    model = QuestionList
    form = QuestionListForm
    extra = 0
    exclude = ["name"]
    show_change_link = True


class ChoiceInline(TranslationTabularInline):
    model = Choice
    extra = 0
    show_change_link = True


@admin.action(description=_("Duplicate selected choice sets"))
def duplicate_choice_list(modeladmin, request, queryset):
    for choice_list in queryset:
        n_choice_lists = ChoiceList.objects.filter(
            identifier__regex=rf'^{choice_list.identifier}(_\d+)*$'
        ).count()
        new_choice_list = ChoiceList.objects.create(
            identifier=f"{choice_list.identifier}_{n_choice_lists}"
        )
        choices = choice_list.choices.all()
        for choice in choices:
            new_choice = deepcopy(choice)
            new_choice.pk = None
            new_choice.choicelist = new_choice_list
            new_choice.save()


class ChoiceListAdmin(TabbedTranslationAdmin):
    model = ChoiceList
    actions = [duplicate_choice_list]
    inlines = [ChoiceInline]
    change_form_template = 'question_change.html'


@admin.action(description=_("Duplicate selected questions"))
def duplicate_question(modeladmin, request, queryset):
    """duplicate questions, appending an integer to the identifier depending on the number of previous copies"""
    for question in queryset:
        n_questions = Question.objects.filter(
            identifier__regex=rf'^{question.identifier}(_\d+)*$'
        ).count()
        question.identifier = f"{question.identifier}_{n_questions}"
        question.from_python = False
        question.save()


@admin.action(description=_("Rescore selected questions"))
def rescore_question(modeladmin, request, queryset):
    """After updating the scoring_rule of a question, rescore all results of that question"""
    for question in queryset:
        results = Result.objects.filter(question_identifier=question.identifier).all()
        for result in results:
            result.scoring_rule = question.profile_scoring_rule
            try:
                result.score = apply_scoring_rule(result, result.json_data)
            except:
                logger.error(f"Could not rescore result {result.pk}: data not defined")
            result.save()


class QuestionAdmin(TabbedTranslationAdmin):

    form = QuestionForm
    actions = [duplicate_question, rescore_question]
    change_form_template = 'question_change.html'

    class Media:
        js = ["question_admin.js"]


class QuestionListAdmin(admin.ModelAdmin):
    inlines = [QuestionInListInline]
    form = QuestionListForm


admin.site.register(ChoiceList, ChoiceListAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionList, QuestionListAdmin)
