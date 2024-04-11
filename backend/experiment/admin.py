import csv
from zipfile import ZipFile
from io import BytesIO
import json
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.core import serializers
from django.shortcuts import render, redirect
from django.forms import CheckboxSelectMultiple, ModelForm, ModelMultipleChoiceField
from django.http import HttpResponse
from inline_actions.admin import InlineActionsModelAdminMixin
from django.urls import reverse
from django.utils.html import format_html
from experiment.models import Experiment, ExperimentSeries, Feedback, Question, QuestionGroup, QuestionSeries, QuestionInSeries
from experiment.forms import ExperimentForm, ExportForm, TemplateForm, EXPORT_TEMPLATES, QuestionSeriesAdminForm
from section.models import Section, Song
from result.models import Result
from participant.models import Participant


class FeedbackInline(admin.TabularInline):
    """Inline to show results linked to given participant
    """

    model = Feedback
    fields = ['text']
    extra = 0


class QuestionInSeriesInline(admin.TabularInline):
    model = QuestionInSeries
    extra = 0

class QuestionSeriesInline(admin.TabularInline):
    model = QuestionSeries
    extra = 0
    show_change_link = True

class QuestionAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return obj.editable if obj else False

class QuestionGroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj and not obj.editable:
            for field_name in form.base_fields:
                form.base_fields[field_name].disabled = True

        return form

class QuestionSeriesAdmin(admin.ModelAdmin):
    inlines = [QuestionInSeriesInline]
    form = QuestionSeriesAdminForm

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(QuestionSeries, QuestionSeriesAdmin)

class ExperimentAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('image_preview', 'experiment_link', 'rules', 'rounds', 'playlist_count',
                    'session_count', 'active')
    list_filter = ['active']
    search_fields = ['name']
    inline_actions = ['export', 'export_csv']
    fields = ['name', 'description', 'image', 'slug', 'url', 'hashtag', 'theme_config',  'language', 'active', 'rules',
              'rounds', 'bonus_points', 'playlists', 'consent']
    inlines = [QuestionSeriesInline, FeedbackInline]
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
    list_display = ('slug', 'name', 'description_excerpt', 'dashboard')
    fields = ['slug', 'name', 'description', 'first_experiments',
              'random_experiments', 'last_experiments', 'dashboard']
    form = ExperimentSeriesForm

    def description_excerpt(self, obj):

        if len(obj.description) < 50:
            return obj.description

        return obj.description[:50] + '...'


admin.site.register(ExperimentSeries, ExperimentSeriesAdmin)
