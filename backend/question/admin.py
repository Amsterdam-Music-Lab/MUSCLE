from copy import deepcopy

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin
from question.models import (
    Choice,
    ChoiceSet,
    Question,
    QuestionSeries,
    QuestionInSeries,
)
from question.forms import QuestionForm


class QuestionInSeriesInline(admin.TabularInline):
    model = QuestionInSeries
    extra = 0


class QuestionSeriesInline(admin.TabularInline):
    model = QuestionSeries
    inlines = [QuestionInSeriesInline]
    extra = 0
    show_change_link = True


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
    show_change_link = True


class ChoiceSetAdmin(admin.ModelAdmin):
    model = ChoiceSet
    inlines = [ChoiceInline]
    change_form_template = 'question_change.html'


@admin.action(description=_("Duplicate selected questions"))
def duplicate_question(modeladmin, request, queryset):
    """duplicate questions, appending an integer to the key depending on the number of previous copies"""
    for question in queryset:
        n_questions = Question.objects.filter(
            key__regex=rf'^{question.key}(_\d+)*$'
        ).count()
        question_copy = deepcopy(question)
        question_copy.key = f"{question.key}_{n_questions}"
        question_copy.save()

class QuestionAdmin(TabbedTranslationAdmin):

    form = QuestionForm
    actions = [duplicate_question]
    change_form_template = 'question_change.html'

    class Media:
        js = ["question_admin.js"]


class QuestionSeriesAdmin(admin.ModelAdmin):
    inlines = [QuestionInSeriesInline]


admin.site.register(ChoiceSet, ChoiceSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSeries, QuestionSeriesAdmin)
