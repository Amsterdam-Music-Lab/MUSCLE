from django.contrib import admin
from django.db import models
from question.models import Question, QuestionGroup, QuestionSeries, QuestionInSeries, Choice
from django.forms import CheckboxSelectMultiple
from experiment.forms import QuestionSeriesAdminForm
from question.forms import QuestionForm


class QuestionInSeriesInline(admin.TabularInline):
    model = QuestionInSeries
    extra = 0


class QuestionSeriesInline(admin.TabularInline):
    model = QuestionSeries
    extra = 0
    show_change_link = True

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    show_change_link = True

class QuestionAdmin(admin.ModelAdmin):

    form = QuestionForm

    def has_change_permission(self, request, obj=None):
        return obj.editable if obj else False

    def get_fields(self, request, obj=None):

        if not obj:
            fields = ["key","question","type"]
        elif not obj.editable:
            fields = ["key","question"]
        else:
            fields = ["key","question","type","explainer"]
            if obj.type == "LikertQuestion":
                fields += ["scale_steps","profile_scoring_rule"]
            elif obj.type == "LikertQuestionIcon":
                fields += ["profile_scoring_rule"]
            elif obj.type in ["NumberQuestion"]:
                fields += ["min_value","max_value"]
            elif obj.type == "TextQuestion":
                fields += ["max_length"]
            elif obj.type == "ChoiceQuestion":
                fields += ["view","min_values"]

        return fields

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
    form = QuestionSeriesAdminForm


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(QuestionSeries, QuestionSeriesAdmin)
