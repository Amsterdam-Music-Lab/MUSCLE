import csv

from inline_actions.admin import InlineActionsModelAdminMixin
from django.contrib import admin, messages
from django.http import JsonResponse, HttpResponse

from .models import Section, Playlist


class SectionAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('artist_name', 'song_name', 'start_time',
                    'play_count', 'playlist', 'code')
    list_filter = [('playlist', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['song__artist', 'song__name', 'playlist__name']
    readonly_fields = ('play_count', 'code')

    # Prevent large inner join
    list_select_related = ()


admin.site.register(Section, SectionAdmin)


class PlaylistAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'section_count', 'experiment_count')
    search_fields = ['name', 'section__song__artist', 'section__song__name']
    inline_actions = ['export_json', 'export_csv']

    def save_model(self, request, obj, form, change):

        # store proces value
        process_csv = obj.process_csv
        if process_csv:
            obj.process_csv = False
        # save playlist (so it sure has an id)
        super().save_model(request, obj, form, change)

        # process csv
        if process_csv:
            csv_result = obj.update_sections()

            # create message based on csv_result (CSV_ERROR or CSV_OK)
            if csv_result['status'] == Playlist.CSV_ERROR:
                messages.add_message(request, messages.ERROR,
                                     csv_result['message'])

            elif csv_result['status'] == Playlist.CSV_OK:
                messages.add_message(request, messages.INFO,
                                     csv_result['message'])

    def export_json(self, request, obj, parent_obj=None):
        """Export playlist data in JSON, force download"""

        response = JsonResponse(
            obj.export_admin(), json_dumps_params={'indent': 4})

        # force download attachment
        response['Content-Disposition'] = 'attachment; filename="playlist_' + \
            str(obj.id)+'.json"'
        return response

    export_json.short_description = "Export JSON"

    def export_csv(self, request, obj, parent_obj=None):
        """Export playlist sections to csv, force download"""

        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        for section in obj.section_set.all():
            writer.writerow(section.export_admin_csv())

        # force download attachment
        response['Content-Disposition'] = 'attachment; filename="playlist_' + \
            str(obj.id)+'.csv"'
        return response

    export_csv.short_description = "Export Sections CSV"


admin.site.register(Playlist, PlaylistAdmin)
