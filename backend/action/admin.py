from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline


from action.models import (
    Explainer,
    Final,
    FinalFeedback,
    FinalScore,
    Progress,
    Step,
)

class StepInline(TranslationTabularInline):
    model = Step
    extra = 0
    show_change_link = True


class ExplainerAdmin(TabbedTranslationAdmin):
    model = Explainer
    inlines = [StepInline]


class FinalFeedbackInline(TranslationTabularInline):
    model = FinalFeedback


class FinalScoreInline(TranslationTabularInline):
    model = FinalScore


class ProgressInline(admin.TabularInline):
    model = Progress


class FinalAdmin(TabbedTranslationAdmin):
    model = Final
    inlines = [FinalFeedbackInline, FinalScoreInline, ProgressInline]


admin.site.register(Explainer, ExplainerAdmin)
admin.site.register(Final, FinalAdmin)
