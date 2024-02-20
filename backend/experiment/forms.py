from django.forms import CheckboxSelectMultiple, ModelForm, ChoiceField, Form, MultipleChoiceField, Select
from experiment.models import Experiment
from experiment.rules import EXPERIMENT_RULES

from django.forms import TypedMultipleChoiceField, CheckboxSelectMultiple
from .questions import QUESTIONS_CHOICES

# session_keys for Export CSV
SESSION_CHOICES = [('experiment_id', 'Experiment ID'),
                   ('experiment_name', 'Experiment name'),
                   ('participant_id', 'Participant ID'),
                   ('participant_country', 'Participant Country'),
                   ('participant_access_info', 'Participant access info'),
                   ('session_start', 'Session start time'),
                   ('session_end', 'Session end time'),
                   ('final_score', 'Final score'),
                   ]

# result_keys for Export CSV
RESULT_CHOICES = [('section_name', 'Section name'),
                  ('result_created_at', 'Created time'),
                  ('result_score', 'Result score'),
                  ('result_comment', 'Result comment'),
                  ('expected_response', 'Expected response'),
                  ('given_response', 'Given response'),
                  ('question_key', 'Question key'),
                  ]

# export_options for Export CSV
EXPORT_OPTIONS = [('export_profile', "Include participants' profile Q&A"),
                  ('session_data', 'Include session data'),
                  ('convert_session_json', 'Convert session data JSON to CSV columns'),
                  ('decision_time', 'Include result decision time'),
                  ('result_config', "Include result configuration parameters"),
                  ('convert_result_json', 'Convert result data JSON to CSV columns'),
                  ('wide_format', 'CSV wide format (Long format is default)'),
                  ]

# Export templates for Export CSV
EXPORT_TEMPLATES = {'wide':
                    [['experiment_id', 'experiment_name', 'participant_id',
                      'participant_country', 'participant_access_info', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['export_profile', 'session_data', 'convert_session_json', 'decision_time', 'result_config',
                      'convert_result_json', 'wide_format']],
                    'wide_json':
                    [['experiment_id', 'experiment_name', 'participant_id',
                      'participant_country', 'participant_access_info', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['export_profile', 'session_data', 'decision_time', 'result_config', 'wide_format']],
                    'wide_results':
                    [['experiment_name', 'participant_id', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['session_data', 'convert_session_json', 'decision_time', 'wide_format']],

                    'wide_results_json':
                    [['experiment_name', 'participant_id', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['session_data', 'decision_time', 'result_config', 'wide_format']],
                    'wide_profile':
                    [['experiment_name', 'participant_id',
                      'participant_country', 'participant_access_info'],
                     [],
                     ['export_profile', 'wide_format']],

                    'long':
                    [['experiment_id', 'experiment_name', 'participant_id',
                      'participant_country', 'participant_access_info', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['export_profile', 'session_data', 'convert_session_json', 'decision_time', 'result_config',
                      'convert_result_json']],
                    'long_json':
                    [['experiment_id', 'experiment_name', 'participant_id',
                      'participant_country', 'participant_access_info', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['export_profile', 'session_data', 'decision_time', 'result_config'
                      ]],
                    'long_results':
                    [['experiment_name', 'participant_id', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['session_data', 'convert_session_json', 'decision_time']],
                    'long_results_json':
                    [['experiment_name', 'participant_id', 'session_start', 'session_end', 'final_score'],
                     ['section_name', 'result_created_at', 'result_score', 'result_comment',
                      'expected_response', 'given_response'],
                     ['session_data', 'decision_time', 'result_config']],
                    'long_profile':
                    [['experiment_name', 'participant_id',
                      'participant_country', 'participant_access_info'],
                     [],
                     ['export_profile']]
                    }

# Export templates for Export CSV (ExportForm)
TEMPLATE_CHOICES = [
    ('wide', 'CSV wide data format, All data'),
    ('wide_json', 'CSV wide data format, All data, Keep JSON'),
    ('wide_results',
     'CSV wide data format, Session data, Results'),
    ('wide_results_json',
     'CSV wide data format, Session data as JSON, Results, Result data as JSON'),
    ('wide_profile',
     'CSV wide data format, Profile Q&A'),
    ('long', 'CSV long data format, All data'),
    ('long_json', 'CSV long data format, All data, Keep JSON'),
    ('long_results',
     'CSV long data format, Session data, Results'),
    ('long_results_json',
     'CSV long data format, Session data as JSON, Results, Result data as JSON'),
    ('long_profile',
     'CSV long data format, Profile Q&A'),
]


class ExperimentForm(ModelForm):
    # TO DO: add "clean_slug" method which checks that slug is NOT
    # "experiment", "participant", "profile"

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        choices = tuple()
        for i in EXPERIMENT_RULES:
            choices += ((i, EXPERIMENT_RULES[i].__name__),)
        choices += (("","---------"),)

        self.fields['rules'] = ChoiceField(
            choices=sorted(choices)
        )

        self.fields['questions'] = TypedMultipleChoiceField(
            choices=QUESTIONS_CHOICES,
            widget=CheckboxSelectMultiple,
            required=False
        )

    class Meta:
        model = Experiment
        fields = ['name', 'slug', 'active', 'rules',
                  'rounds', 'bonus_points', 'playlists']

    class Media:
        js = ["experiment_admin.js"]
        css = {"all": ["experiment_admin.css"]}


class ExportForm(Form):
    export_session_fields = MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=SESSION_CHOICES
    )
    export_result_fields = MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=RESULT_CHOICES
    )
    export_options = MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=EXPORT_OPTIONS,
    )


class TemplateForm(Form):
    select_template = ChoiceField(
        widget=Select,
        choices=TEMPLATE_CHOICES)
