import csv

from inline_actions.admin import InlineActionsModelAdminMixin
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import audioread

from .models import Section, Playlist, Song
from .forms import AddSections

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

# @admin.register(Playlist)

class SongAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('artist', 'name')    
    search_fields = ['artist', 'name']   

    # Prevent large inner join
    list_select_related = ()

admin.site.register(Song, SongAdmin)

class PlaylistAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'section_count', 'experiment_count')
    search_fields = ['name', 'section__song__artist', 'section__song__name']
    inline_actions = ['add_sections',
                      'edit_sections', 'export_json', 'export_csv']

    def save_model(self, request, obj, form, change):

        # store proces value
        process_csv = obj.process_csv
        
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
        """Add multiple sections
        """
        sections = Section.objects.filter(playlist=obj)
        form = AddSections()
        # Get the info for new sections
        if '_add' in request.POST:
            this_artist = request.POST.get('artist')
            this_name = request.POST.get('name')
            this_tag = request.POST.get('tag')
            this_group = request.POST.get('group')
            new_sections = request.FILES.getlist('files')
            # Create section object for each file
            for section in new_sections:
                new_section = Section.objects.create(playlist=obj,
                                                     tag=this_tag,
                                                     group=this_group,
                                                     filename=section)
                try:
                    new_section.clean_fields()
                except ValidationError as e:
                    new_section.delete()
                    file_errors = form.errors.get('file', [])
                    file_errors.append(_('Cannot upload {}: {}').format(str(section), e.messages[0]))
                    form.errors['file'] = file_errors
                    continue
                if this_artist and this_name:
                    this_song, created = Song.objects.get_or_create(artist=this_artist, name=this_name)
                    new_section.song = this_song                
                file_path = settings.MEDIA_ROOT + '/' + str(new_section.filename)      
                with audioread.audio_open(file_path) as f:
                    new_section.duration = f.duration
                new_section.save()
                obj.save()
            if not form.errors:
                return redirect('/admin/section/playlist')
        # Go back to admin playlist overview
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
        """Edit multiple section in a playlist
        """
        sections = Section.objects.filter(playlist=obj)
        # Get form data for each section in the playlist
        if '_update' in request.POST:
            for section in sections:
                # Create pre fix to get the right section fields
                pre_fix = str(section.id)
                # Get data and update section                                 
                this_artist = request.POST.get(pre_fix + '_artist')
                this_name = request.POST.get(pre_fix + '_name')
                if this_artist and this_name:
                    this_song, created = Song.objects.get_or_create(artist=this_artist, name=this_name)
                    if created:
                        section.song = this_song
                    else:
                        section.song = this_song                                                
                        if request.POST.get(pre_fix + '_restricted'):
                            section.song.restricted = [{"restricted": "nl"}]                            
                        else:
                            section.song.restricted = []
                        section.song.save()
                section.start_time = request.POST.get(pre_fix + '_start_time')
                section.duration = request.POST.get(pre_fix + '_duration')
                section.tag = request.POST.get(pre_fix + '_tag')
                section.group = request.POST.get(pre_fix + '_group')                                
                section.save()
                obj.save()
            return redirect('/admin/section/playlist')
        # Go back to admin playlist overview
        if '_back' in request.POST:
            return redirect('/admin/section/playlist')
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
