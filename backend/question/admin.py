from django.contrib import admin
from django.db import models
from question.models import Question, QuestionGroup, QuestionSeries, QuestionInSeries
from django.forms import CheckboxSelectMultiple
from experiment.forms import QuestionSeriesAdminForm


class QuestionInSeriesInline(admin.TabularInline):
    model = QuestionInSeries
    extra = 0


class QuestionSeriesInline(admin.TabularInline):
    model = QuestionSeries
    extra = 0
    show_change_link = True


class QuestionAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return obj.editable if obj else False


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
