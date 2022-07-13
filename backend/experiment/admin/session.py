from django.contrib import admin
from experiment.models import Session, Result


class ResultInline(admin.TabularInline):
    """Result inline admin for SessionAdmin"""

    model = Result
    extra = 0

    # Field section is excluded from 'fields'
    # If it is added in the future, only show the raw_id
    # To not load a huge list of sections
    raw_id_fields = ("section",)

    fields = ['section', 'created_at', 'score', 'expected_response', 'given_response', 'json_data']


class SessionAdmin(admin.ModelAdmin):
    list_per_page = 50
    inlines = [ResultInline]
    list_display = ('experiment',
                    'playlist',
                    'started_at',
                    'finished_at',
                    'result_count',
                    'final_score')

    # experiment/playlist list_filter will only show up when there are >= 2 choices available
    list_filter = [
        ('experiment', admin.RelatedOnlyFieldListFilter),
        ('playlist', admin.RelatedOnlyFieldListFilter),
        'started_at',
        'finished_at',
    ]


admin.site.register(Session, SessionAdmin)
