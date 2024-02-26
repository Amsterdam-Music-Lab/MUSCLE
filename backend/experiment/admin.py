import csv
from zipfile import ZipFile
from io import BytesIO
import json

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.core import serializers
from django.shortcuts import render, redirect
from django.forms import CheckboxSelectMultiple, ModelForm, ModelMultipleChoiceField
from django.http import HttpResponse
from inline_actions.admin import InlineActionsModelAdminMixin
from experiment.models import Experiment, ExperimentSeries, Feedback
from experiment.forms import ExperimentForm, ExportForm, TemplateForm, EXPORT_TEMPLATES
from section.models import Section, Song
from result.models import Result
from participant.models import Participant


class FeedbackInline(admin.TabularInline):
    """Inline to show results linked to given participant
    """

    model = Feedback
    fields = ['text']
    extra = 0


class ExperimentAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'rules', 'rounds', 'playlist_count',
                    'session_count', 'active')
    list_filter = ['active']
    search_fields = ['name']
    inline_actions = ['export', 'export_csv']
    fields = ['name', 'slug', 'url', 'hashtag', 'language', 'active', 'rules',
              'rounds', 'bonus_points', 'playlists', 'consent', 'questions']
    inlines = [FeedbackInline]
    form = ExperimentForm

    # make playlists fields a list of checkboxes
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def export(self, request, obj, parent_obj=None):
        """Export experiment JSON data as zip archive, force download"""

        # Init empty querysets
        all_results = Result.objects.none()
        all_songs = Song.objects.none()
        all_sections = Section.objects.none()
        all_participants = Participant.objects.none()
        all_profiles = Result.objects.none()

        # Collect data
        all_sessions = obj.export_sessions().order_by('pk')

        for session in all_sessions:
            all_results |= session.export_results()
            all_participants |= Participant.objects.filter(pk=session.participant.pk)
            all_profiles |= session.participant.export_profiles()

        for playlist in obj.playlists.all():
            these_sections = playlist.export_sections()
            all_sections |= these_sections
            for section in these_sections:
                if section.song:
                    all_songs |= Song.objects.filter(pk=section.song.pk)

        # create empty zip file in memory
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as new_zip:
            # serialize data to new json files within the zip file
            new_zip.writestr('sessions.json', data=str(serializers.serialize("json", all_sessions)))
            new_zip.writestr('participants.json', data=str(serializers.serialize("json", all_participants.order_by('pk'))))
            new_zip.writestr('profiles.json', data=str(serializers.serialize("json", all_profiles.order_by('participant', 'pk'))))
            new_zip.writestr('results.json', data=str(serializers.serialize("json", all_results.order_by('session'))))
            new_zip.writestr('sections.json', data=str(serializers.serialize("json", all_sections.order_by('playlist', 'pk'))))
            new_zip.writestr('songs.json', data=str(serializers.serialize("json", all_songs.order_by('pk'))))

        # create forced download response
        response = HttpResponse(zip_buffer.getbuffer())
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = 'attachment; filename="'+obj.slug+'-'+timezone.now().isoformat()+'.zip"'        
        return response

    export.short_description = "Export JSON"

    def export_csv(self, request, obj, parent_obj=None):
        """Export experiment data in CSV, force download"""
        # Handle export command from intermediate form
        if '_export' in request.POST:
            session_keys = []
            result_keys = []
            export_options = []
            # Get all export options
            session_keys = [key for key in request.POST.getlist(
                'export_session_fields')]
            result_keys = [key for key in request.POST.getlist(
                'export_result_fields')]
            export_options = [
                key for key in request.POST.getlist('export_options')]

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
                obj.slug)
            # Get filtered data
            experiment_table, fieldnames = obj.export_table(
                session_keys, result_keys, export_options)
            fieldnames.sort()
            writer = csv.DictWriter(response, fieldnames)
            writer.writeheader()
            writer.writerows(experiment_table)
            return response
        # Go back to admin experiment overview
        if '_back' in request.POST:
            return redirect('/admin/experiment/experiment')
        # Load a template in the export form
        if '_template' in request.POST:
            selected_template = request.POST.get('select_template')
        else:
            selected_template = 'wide'

        initial_fields = {'export_session_fields': EXPORT_TEMPLATES[selected_template][0],
                          'export_result_fields': EXPORT_TEMPLATES[selected_template][1],
                          'export_options': EXPORT_TEMPLATES[selected_template][2]
                          }
        form = ExportForm(
            initial=initial_fields)
        template_form = TemplateForm(
            initial={'select_template': selected_template})
        return render(
            request,
            'csv-export.html',
            context={'experiment': obj,
                     'form': form,
                     'template_form': template_form}
        )

    export_csv.short_description = "Export CSV"


admin.site.register(Experiment, ExperimentAdmin)


class ModelFormFieldAsJSON(ModelMultipleChoiceField):
    """ override clean method to prevent pk lookup to save querysets """
    def clean(self, value):
        return value


class ExperimentSeriesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        experiments = Experiment.objects.all()
        self.fields['first_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)
        self.fields['random_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)
        self.fields['last_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)

    class Meta:
        model = ExperimentSeries
        fields = ['slug', 'first_experiments',
                  'random_experiments', 'last_experiments', 'dashboard']


class ExperimentSeriesAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    fields = ['slug', 'first_experiments',
              'random_experiments', 'last_experiments', 'dashboard']
    form = ExperimentSeriesForm


admin.site.register(ExperimentSeries, ExperimentSeriesAdmin)
