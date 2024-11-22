from django.contrib import admin
from participant.models import Participant
from result.models import Result


class ResultInline(admin.TabularInline):
    """Inline to show results linked to given participant"""

    model = Result
    fields = ["created_at", "question_key", "given_response"]
    extra = 0


class ParticipantAdmin(admin.ModelAdmin):
    inlines = [ResultInline]
    list_per_page = 50
    search_fields = ["unique_hash", "id", "country_code"]
    list_display = (
        "__str__",
        "country_code",
        "session_count",
    )
    list_filter = [("session__block", admin.RelatedOnlyFieldListFilter)]


admin.site.register(Participant, ParticipantAdmin)
