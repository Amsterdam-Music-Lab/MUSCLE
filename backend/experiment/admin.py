import csv

from django.contrib import admin
from django.db import models
from django.shortcuts import render, redirect
from django.forms import CheckboxSelectMultiple, ModelForm, ModelMultipleChoiceField
from django.http import HttpResponse, JsonResponse
from inline_actions.admin import InlineActionsModelAdminMixin
from experiment.models import Experiment, ExperimentSeries
from experiment.forms import ExperimentForm, ExportForm, TemplateForm, EXPORT_TEMPLATES

class ExperimentAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'rules', 'rounds', 'playlist_count',
                    'session_count', 'active')
    list_filter = ['active']
    search_fields = ['name']
    inline_actions = ['export', 'export_csv']
    fields = ['name', 'slug', 'language', 'active', 'rules',
              'rounds', 'bonus_points', 'playlists', 'experiment_series']
    form = ExperimentForm

    # make playlists fields a list of checkboxes
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def export(self, request, obj, parent_obj=None):
        """Export experiment data in JSON, force download"""

        response = JsonResponse(
            obj.export_admin(), json_dumps_params={'indent': 4})

        # force download attachment
        response['Content-Disposition'] = 'attachment; filename="' + \
            obj.slug+'.json"'
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
            context={'form': form,
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
        from . import Experiment
        experiments = Experiment.objects.all().filter(experiment_series=None)
        self.fields['first_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)
        self.fields['random_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)
        self.fields['last_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)

    class Meta:
        model = ExperimentSeries
        fields = ['name', 'first_experiments', 'random_experiments', 'last_experiments']

class ExperimentSeriesAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    fields = ['name', 'first_experiments', 'random_experiments', 'last_experiments']
    form = ExperimentSeriesForm

admin.site.register(ExperimentSeries, ExperimentSeriesAdmin)
