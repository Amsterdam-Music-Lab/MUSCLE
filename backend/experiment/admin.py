import csv
from zipfile import ZipFile
from io import BytesIO
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.core import serializers
from django.shortcuts import render, redirect
from django.forms import CheckboxSelectMultiple, ModelForm, TextInput
from django.http import HttpResponse
from inline_actions.admin import InlineActionsModelAdminMixin
from django.urls import reverse
from django.utils.html import format_html
from experiment.models import Experiment, ExperimentSeries, ExperimentSeriesGroup, Feedback, GroupedExperiment
from experiment.forms import ExperimentSeriesForm, ExperimentForm, ExportForm, TemplateForm, EXPORT_TEMPLATES
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
    list_display = ('image_preview', 'experiment_link', 'rules', 'rounds', 'playlist_count',
                    'session_count', 'active')
    list_filter = ['active']
    search_fields = ['name']
    inline_actions = ['export', 'export_csv']
    fields = ['name', 'description', 'image', 'slug', 'url', 'hashtag', 'theme_config',  'language', 'active', 'rules',
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

    def image_preview(self, obj):
        if obj.image and obj.image.file:
            img_src = obj.image.file.url
            return mark_safe(f'<img src="{img_src}" style="max-height: 50px;"/>')
        return ""
    
    def experiment_link(self, obj):
        """Generate a link to the experiment's admin change page."""
        url = reverse("admin:experiment_experiment_change", args=[obj.pk])
        name = obj.name or obj.slug or "No name"
        return format_html('<a href="{}">{}</a>', url, name)


admin.site.register(Experiment, ExperimentAdmin)


class GroupedExperimentInline(admin.StackedInline):
    model = GroupedExperiment
    extra = 0


class ExperimentSeriesGroupInline(admin.StackedInline):
    model = ExperimentSeriesGroup
    extra = 0
    inlines = [GroupedExperimentInline]


class ExperimentSeriesAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('slug', 'name', 'description_excerpt', 'dashboard', 'groups')
    fields = ['slug', 'name', 'description', 'theme_config', 'first_experiments',
              'random_experiments', 'last_experiments', 'dashboard',
              'about_content']
    form = ExperimentSeriesForm
    inlines = [ExperimentSeriesGroupInline]

    def description_excerpt(self, obj):

        if len(obj.description) < 50:
            return obj.description

        return obj.description[:50] + '...'

    def groups(self, obj):
        groups = ExperimentSeriesGroup.objects.filter(series=obj)
        return format_html(', '.join([f'<a href="/admin/experiment/experimentseriesgroup/{group.id}/change/">{group.name}</a>' for group in groups]))


admin.site.register(ExperimentSeries, ExperimentSeriesAdmin)


class ExperimentSeriesGroupAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name_link', 'related_series', 'order', 'dashboard', 'randomize', 'experiments')
    fields = ['name', 'series', 'order', 'dashboard', 'randomize']
    inlines = [GroupedExperimentInline]

    def name_link(self, obj):
        obj_name = obj.__str__()
        url = reverse("admin:experiment_experimentseriesgroup_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj_name)

    def related_series(self, obj):
        url = reverse("admin:experiment_experimentseries_change", args=[obj.series.pk])
        return format_html('<a href="{}">{}</a>', url, obj.series.name)

    def experiments(self, obj):
        experiments = GroupedExperiment.objects.filter(group=obj)

        if not experiments:
            return "No experiments"

        return format_html(', '.join([f'<a href="/admin/experiment/groupedexperiment/{experiment.id}/change/">{experiment.experiment.name}</a>' for experiment in experiments]))


admin.site.register(ExperimentSeriesGroup, ExperimentSeriesGroupAdmin)
