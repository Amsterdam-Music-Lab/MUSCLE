from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField
from inline_actions.admin import InlineActionsModelAdminMixin

from experiment.models import ExperimentSeries

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
