import csv
import json

from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple, ModelForm, ModelMultipleChoiceField, ChoiceField
from django.http import HttpResponse, JsonResponse
from inline_actions.admin import InlineActionsModelAdminMixin
from experiment.models import Experiment
from experiment.rules import EXPERIMENT_RULES

class ModelFormFieldAsJSON(ModelMultipleChoiceField):
    """ override clean method to prevent pk lookup to save querysets """
    def clean(self, value):
        return value

class ExperimentForm(ModelForm):
    # TO DO: add "clean_slug" method which checks that slug is NOT 
    # "experiment", "participant", "profile"

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        choices = tuple()
        for i in EXPERIMENT_RULES:
            choices += ((i, EXPERIMENT_RULES[i].__name__),)

        self.fields['rules'] = ChoiceField(
            choices=choices
        )
        experiments = Experiment.objects.all()
        self.fields['nested_experiments'] = ModelFormFieldAsJSON(queryset=experiments, required=False)

    class Meta:
        model = Experiment
        fields = ['name', 'slug', 'active', 'rules',
                  'rounds', 'bonus_points', 'playlists']


class ExperimentAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'rules', 'rounds', 'playlist_count',
                    'session_count', 'active')
    list_filter = ['active']
    search_fields = ['name']
    inline_actions = ['export', 'export_csv']
    fields = ['name', 'slug', 'language', 'active', 'rules',
              'rounds', 'bonus_points', 'playlists', 'nested_experiments']
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

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(obj.slug)

        experiment_table, fieldnames = obj.export_table()
        fieldnames.sort()
        writer = csv.DictWriter(response, fieldnames)
        writer.writeheader()
        writer.writerows(experiment_table)

        return response
    
    export_csv.short_description = "Export CSV"


admin.site.register(Experiment, ExperimentAdmin)
