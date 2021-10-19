from django.contrib import admin
from experiment.models import Section


class SectionAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('artist', 'name', 'start_time',
                    'play_count', 'playlist', 'code')
    list_filter = [('playlist', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['artist', 'name', 'playlist__name']
    readonly_fields = ('play_count', 'code')

    # Prevent large inner join
    list_select_related = ()


admin.site.register(Section, SectionAdmin)
