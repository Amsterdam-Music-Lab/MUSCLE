from copy import deepcopy

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


class QuestionInListInline(admin.TabularInline):
    model = QuestionInList
    extra = 0


class QuestionListInline(admin.TabularInline):
    model = QuestionList
    inlines = [QuestionInListInline]
    readonly_fields = ["name"]
    extra = 0
    show_change_link = True


class ChoiceInline(TranslationTabularInline):
    model = Choice
    extra = 0
    show_change_link = True


@admin.action(description=_("Duplicate selected choice sets"))
def duplicate_choice_list(modeladmin, request, queryset):
    for choice_list in queryset:
        n_choice_lists = ChoiceList.objects.filter(
            key__regex=rf'^{choice_list.key}(_\d+)*$'
        ).count()
        new_choice_list = ChoiceList.objects.create(
            key=f"{choice_list.key}_{n_choice_lists}"
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


class QuestionListAdmin(admin.ModelAdmin):
    inlines = [QuestionInListInline]
    form = QuestionListForm


admin.site.register(ChoiceList, ChoiceListAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionList, QuestionListAdmin)
