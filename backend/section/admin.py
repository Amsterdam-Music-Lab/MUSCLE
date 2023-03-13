import csv
import audioread

from inline_actions.admin import InlineActionsModelAdminMixin
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from .models import Section, Playlist
from section.forms import AddSections


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

# @admin.register(Playlist)


class PlaylistAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'section_count', 'experiment_count')
    search_fields = ['name', 'section__artist', 'section__name']
    inline_actions = ['add_sections',
                      'edit_sections', 'export_json', 'export_csv']

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

    def add_sections(self, request, obj, parent_obj=None):
        form = AddSections
        sections = Section.objects.filter(playlist=obj)
        if '_add' in request.POST:
            this_artist = request.POST.get('artist')
            this_name = request.POST.get('name')
            this_tag = request.POST.get('tag')
            this_group = request.POST.get('group')
            new_sections = request.FILES.getlist('files')
            for section in new_sections:
                
                new_section = Section.objects.create(playlist=obj,
                                                     artist=this_artist,
                                                     name=this_name,
                                                     tag=this_tag,
                                                     group=this_group,
                                                     filename=section)                
                new_section.save()
                # with audioread.audio_open(new_section.filename.url) as f:
                #     new_section.duration = f.duration                
                # new_section.save()             
         # Go back to admin experiment overview
        if '_back' in request.POST:
            return redirect('/admin/section/playlist')
        return render(
            request,
            'add-sections.html',
            context={'playlist': obj,
                     'sections': sections,
                     'form': form}
        )

    def edit_sections(self, request, obj, parent_obj=None):
        sections = Section.objects.filter(playlist=obj)
        if '_update' in request.POST:
            this_artist = request.POST.get('artist')
            this_name = request.POST.get('name')
            this_tag = request.POST.get('tag')
            this_group = request.POST.get('group')
        return render(
            request,
            'edit-sections.html',
            context={'playlist': obj,
                     'sections': sections}
        )

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
