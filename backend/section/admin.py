import csv
from os import listdir
from os.path import isdir, join
from zipfile import ZipFile

from inline_actions.admin import InlineActionsModelAdminMixin
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

import audioread
import sys

from .models import Section, Playlist, Song
from .forms import AddSections, PlaylistAdminForm
from .utils import get_or_create_song


class SectionAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        "artist_name",
        "song_name",
        "start_time",
        "play_count",
        "playlist",
    )
    list_filter = [("playlist", admin.RelatedOnlyFieldListFilter)]
    search_fields = ["song__artist", "song__name", "playlist__name"]
    readonly_fields = ["play_count"]
    autocomplete_fields = ["song"]

    # Prevent large inner join
    list_select_related = ()


class SongAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ("artist", "name")
    search_fields = ["artist", "name"]

    # Prevent large inner join
    list_select_related = ()

    def has_module_permission(self, request):
        '''Prevents the admin from being shown in the sidebar.'''
        return False


@admin.action(description="Export selected playlists")
def playlist_export(modeladmin, request, queryset: QuerySet[Playlist]):
    response = HttpResponse(content_type='application/zip')
    zip_file = ZipFile(response, 'w')
    for playlist in queryset:
        # write csv data
        zip_file.writestr(f"{playlist.name}.csv", data=playlist.csv)
        uploads = join(settings.MEDIA_ROOT, playlist.get_upload_path())
        if not isdir(uploads):
            continue
        for audio_file in listdir(uploads):
            zip_file.write(join(uploads, audio_file))
    response['Content-Disposition'] = 'attachment; filename=playlists.zip'
    return response


class PlaylistAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    form = PlaylistAdminForm
    change_form_template = "change_form.html"
    actions = [playlist_export]
    list_display = ("name", "_section_count", "_block_count")
    search_fields = ["name", "section__song__artist", "section__song__name"]
    inline_actions = ["add_sections", "edit_sections", "export_csv"]

    def redirect_to_overview(self):
        return redirect(reverse("admin:section_playlist_changelist"))

    def save_model(self, request, obj, form, change):
        # store proces value
        process_csv = obj.process_csv

        # save playlist (so it sure has an id)
        super().save_model(request, obj, form, change)

        # process csv
        if process_csv:
            csv_result = obj._update_sections()

            # create message based on csv_result (CSV_ERROR or CSV_OK)
            if csv_result["status"] == Playlist.CSV_ERROR:
                for message in csv_result["messages"]:
                    messages.add_message(request, messages.ERROR, message)

            elif csv_result["status"] == Playlist.CSV_OK:
                messages.add_message(request, messages.INFO, csv_result["message"])

    def add_sections(self, request, obj, parent_obj=None):
        """Add multiple sections"""
        sections = Section.objects.filter(playlist=obj)
        form = AddSections()
        # Get the info for new sections
        if "_add" in request.POST:
            this_artist = request.POST.get("artist")
            this_name = request.POST.get("name")
            this_tag = request.POST.get("tag")
            this_group = request.POST.get("group")
            new_sections = request.FILES.getlist("files")
            # Create section object for each file
            for section in new_sections:
                new_section = Section.objects.create(
                    playlist=obj, tag=this_tag, group=this_group, filename=section
                )
                try:
                    new_section.clean_fields()
                except ValidationError as e:
                    new_section.delete()
                    file_errors = form.errors.get("file", [])
                    file_errors.append(
                        _("Cannot upload {}: {}").format(str(section), e.messages[0])
                    )
                    form.errors["file"] = file_errors
                    continue

                # Retrieve or create Song object
                song = None
                if this_artist or this_name:
                    song = get_or_create_song(this_artist, this_name)
                new_section.song = song

                file_path = join(settings.MEDIA_ROOT, str(new_section.filename))
                with audioread.audio_open(file_path) as f:
                    new_section.duration = f.duration
                new_section.save()

            obj.save()
            if not form.errors:
                return self.redirect_to_overview()
        # Go back to admin playlist overview
        if "_back" in request.POST:
            return self.redirect_to_overview()
        return render(
            request,
            "add-sections.html",
            context={"playlist": obj, "sections": sections, "form": form},
        )

    def edit_sections(self, request, obj, parent_obj=None):
        """Edit multiple section in a playlist"""
        sections = Section.objects.filter(playlist=obj)
        # Get form data for each section in the playlist
        if "_update" in request.POST:
            for section in sections:
                # Create pre fix to get the right section fields
                pre_fix = str(section.id)
                # Get data and update section
                this_artist = request.POST.get(pre_fix + "_artist")
                this_name = request.POST.get(pre_fix + "_name")

                # Retrieve or create Song object
                song = None
                if this_artist or this_name:
                    song = get_or_create_song(this_artist, this_name)
                section.song = song

                section.start_time = request.POST.get(pre_fix + "_start_time")

                new_duration = float(request.POST.get(pre_fix + "_duration"))
                # while running tests this would throw an error
                if "test" not in sys.argv:
                    # Check if the duration in the csv exceeds the actual duration of the audio file
                    file_path = join(settings.MEDIA_ROOT, str(section.filename))

                    # while running tests this would throw an error
                    with audioread.audio_open(file_path) as f:
                        actual_duration = f.duration
                    if new_duration > actual_duration:
                        # Add or edit this row, but show an error message containing the actual saved duration
                        section.duration = actual_duration

                        messages.error(request, f"Error: The duration of {section.filename} exceeds the actual duration of the audio file and has been set to {actual_duration} seconds.")
                    else:
                        section.duration = new_duration
                else:
                    section.duration = new_duration

                section.tag = request.POST.get(pre_fix + "_tag")
                section.group = request.POST.get(pre_fix + "_group")
                section.save()
            obj.process_csv = False
            obj.save()
            return self.redirect_to_overview()
        if "_back" in request.POST:
            return self.redirect_to_overview()
        return render(
            request,
            "edit-sections.html",
            context={"playlist": obj, "sections": sections},
        )

    def export_csv(self, request, obj, parent_obj=None):
        """Export playlist sections to csv, force download"""

        response = HttpResponse(content_type="text/csv")

        writer = csv.writer(response)
        for section in obj.section_set.values_list(
            "song__artist",
            "song__name",
            "start_time",
            "duration",
            "filename",
            "tag",
            "group",
        ):
            writer.writerow(section)

        # force download attachment
        response["Content-Disposition"] = (
            'attachment; filename="playlist_' + str(obj.id) + '.csv"'
        )
        return response

    export_csv.short_description = "Export Sections CSV"

    def export_csv_view(self, request, pk):
        obj = self.get_object(request, pk)
        return self.export_csv(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/export_csv/",
                self.export_csv_view,
                name="section_playlist_export_csv",
            ),
        ]
        return custom_urls + urls


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Song, SongAdmin)
