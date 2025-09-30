from copy import deepcopy

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline

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
    extra = 0
    show_change_link = True


class ChoiceInline(TranslationStackedInline):
    model = Choice
    extra = 0
    show_change_link = True


class ChoiceSetAdmin(admin.ModelAdmin):
    model = ChoiceSet
    inlines = [ChoiceInline]


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

    def get_fieldsets(self, request, obj=None):

        fieldsets = super().get_fieldsets(request, obj)

        fields = fieldsets[0][1]["fields"]
        fields_to_show = set() # in addition to key, question(_lang), explainer(_lang), type
        fields_to_remove_all = {
            'profile_scoring_rule',
            'min_value',
            'max_value',
            'max_length',
            'min_values',
        }
        fields_to_remove_extra = set()

        choice_types = [
            "AutoCompleteQuestion",
            "ButtonArrayQuestion",
            "CheckboxQuestion",
            "DropdownQuestion",
            "IconRangeQuestion",
            "RadiosQuestion",
            "TextRangeQuestion",
        ]
        if obj:
            if obj.type in choice_types:
                fields_to_show = {"choices", "profile_scoring_rule"}
                if obj.type == "CheckboxQuestion":
                    fields_to_show.update({"min_values"})
            elif obj.type in ["NumberQuestion", "RangeQuestion"]:
                fields_to_show = {"min_value","max_value"}
            elif obj.type == "TextQuestion":
                fields_to_show = {"max_length"}

        fields_to_remove = (fields_to_remove_all - fields_to_show) | fields_to_remove_extra
        for f in fields_to_remove:
            fields.remove(f)

        return fieldsets


class QuestionSeriesAdmin(admin.ModelAdmin):
    inlines = [QuestionInSeriesInline]
    form = QuestionSeriesForm


admin.site.register(ChoiceSet, ChoiceSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSeries, QuestionSeriesAdmin)
