from django.contrib import admin
from experiment.models import Participant, Session


class SessionInline(admin.TabularInline):
    """Session inline admin for ParticipantAdmin
    TO DO: show profile type results here instead
    """

    model = Session
    extra = 0


class ParticipantAdmin(admin.ModelAdmin):
    inlines = [SessionInline]
    list_per_page = 50
    search_fields = ['unique_hash', 'id', 'country_code']
    list_display = ('__str__',
                    'country_code',
                    'session_count',
                    )
    list_filter = [
        ('session__experiment', admin.RelatedOnlyFieldListFilter)
    ]


admin.site.register(Participant, ParticipantAdmin)
