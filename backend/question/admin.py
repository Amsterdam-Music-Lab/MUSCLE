from copy import deepcopy

from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from nested_admin import NestedTabularInline
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from question.models import (
    Question,
    QuestionGroup,
    QuestionSeries,
    QuestionInSeries,
    Choice,
)
from question.forms import QuestionForm, QuestionSeriesForm


class QuestionInSeriesInline(NestedTabularInline):
    model = QuestionInSeries
    extra = 0


class QuestionSeriesInline(NestedTabularInline):
    model = QuestionSeries
    inlines = [QuestionInSeriesInline]
    extra = 0
    show_change_link = True

    template = 'admin/question_series.html'


class ChoiceInline(TranslationTabularInline):
    model = Choice
    extra = 0
    show_change_link = True


@admin.action(description=_("Duplicate selected questions"))
def duplicate_question(modeladmin, request, queryset):
    questions = queryset
    for question in questions:
        question_copy = deepcopy(question)
        question_copy.key = f"{question.key}_copy"
        question_copy.save()
        if question.choice_set.count():
            for choice in list(question.choice_set.all()):
                choice_copy = choice
                choice_copy.pk = None
                choice_copy._state.adding = True
                choice_copy.question = question_copy
                choice_copy.save()


class QuestionAdmin(TabbedTranslationAdmin):

    form = QuestionForm
    actions = [duplicate_question]

    def get_fieldsets(self, request, obj=None):

        fieldsets = super().get_fieldsets(request, obj)

        fields = fieldsets[0][1]["fields"]
        fields_to_show = set() # in addition to key, question(_lang), explainer(_lang), type
        fields_to_remove_all = {'scale_steps', 'profile_scoring_rule', 'min_value', 'max_value', 'max_length', 'min_values', 'view'}
        fields_to_remove_extra = set()

        if obj:
            if obj.type == "LikertQuestion":
                fields_to_show = {"scale_steps","profile_scoring_rule"}
            elif obj.type == "LikertQuestionIcon":
                fields_to_show = {"profile_scoring_rule"}
            elif obj.type in ["NumberQuestion"]:
                fields_to_show = {"min_value","max_value"}
            elif obj.type == "TextQuestion":
                fields_to_show = {"max_length"}
            elif obj.type == "ChoiceQuestion":
                fields_to_show = {"view","min_values"}

        fields_to_remove = (fields_to_remove_all - fields_to_show) | fields_to_remove_extra
        for f in fields_to_remove:
            fields.remove(f)

        return fieldsets

    def get_inlines(self, request, obj=None):

        inlines = []
        if obj and obj.type in ("LikertQuestion","BooleanQuestion","AutoCompleteQuestion","ChoiceQuestion"):
            inlines = [ChoiceInline]
        return inlines


class QuestionGroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def get_form(self, request, obj=None, **kwargs):
        """This method is needed because setting the QuestionGroup.questions field as readonly
            for built-in (i.e., not editable) groups shows the questions as one-line of concatenated strings, which is ugly.
            Instead, this method allows to keep the checkboxes, but disabled"""
        form = super().get_form(request, obj, **kwargs)

        if obj and not obj.editable:
            for field_name in form.base_fields:
                form.base_fields[field_name].disabled = True

        return form


class QuestionSeriesAdmin(admin.ModelAdmin):
    inlines = [QuestionInSeriesInline]
    form = QuestionSeriesForm


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(QuestionSeries, QuestionSeriesAdmin)
