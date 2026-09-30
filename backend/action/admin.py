from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline


from action.models import (
    Explainer,
    Final,
    Step,
)

class StepInline(TranslationTabularInline):
    model = Step
    extra = 0
    show_change_link = True


class ExplainerAdmin(TabbedTranslationAdmin):
    model = Explainer
    inlines = [StepInline]


class FinalAdmin(TabbedTranslationAdmin):
    model = Final


admin.site.register(Explainer, ExplainerAdmin)
admin.site.register(Final, FinalAdmin)
