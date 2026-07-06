from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from action.models import Explainer, Step


class StepInline(TranslationTabularInline):
    model = Step
    extra = 0
    show_change_link = True


class ExplainerAdmin(TabbedTranslationAdmin):
    model = Explainer
    inlines = [StepInline]


admin.site.register(Explainer, ExplainerAdmin)
