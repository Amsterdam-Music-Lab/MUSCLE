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
from question.forms import QuestionForm, QuestionSeriesForm


class QuestionInSeriesInline(admin.TabularInline):
    model = QuestionInSeries
    extra = 0


class QuestionSeriesInline(admin.TabularInline):
    model = QuestionSeries
    inlines = [QuestionInSeriesInline]
    readonly_fields = ["name"]
    extra = 0
    show_change_link = True


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
    show_change_link = True


@admin.action(description=_("Duplicate selected choice sets"))
def duplicate_choice_set(modeladmin, request, queryset):
    for choice_set in queryset:
        n_choice_sets = ChoiceSet.objects.filter(
            key__regex=rf'^{choice_set.key}(_\d+)*$'
        ).count()
        new_choice_set = ChoiceSet.objects.create(
            key=f"{choice_set.key}_{n_choice_sets}"
        )
        choices = choice_set.choices.all()
        for choice in choices:
            new_choice = deepcopy(choice)
            new_choice.pk = None
            new_choice.set = new_choice_set
            new_choice.save()


class ChoiceSetAdmin(admin.ModelAdmin):
    model = ChoiceSet
    actions = [duplicate_choice_set]
    inlines = [ChoiceInline]
    change_form_template = 'question_change.html'


@admin.action(description=_("Duplicate selected questions"))
def duplicate_question(modeladmin, request, queryset):
    """duplicate questions, appending an integer to the key depending on the number of previous copies"""
    for question in queryset:
        n_questions = Question.objects.filter(
            key__regex=rf'^{question.key}(_\d+)*$'
        ).count()
        question.key = f"{question.key}_{n_questions}"
        question.save()

class QuestionAdmin(TabbedTranslationAdmin):

    form = QuestionForm
    actions = [duplicate_question]
    change_form_template = 'question_change.html'

    class Media:
        js = ["question_admin.js"]


class QuestionSeriesAdmin(admin.ModelAdmin):
    inlines = [QuestionInSeriesInline]
    form = QuestionSeriesForm


admin.site.register(ChoiceSet, ChoiceSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSeries, QuestionSeriesAdmin)
