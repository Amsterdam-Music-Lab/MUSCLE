from django.forms import CheckboxSelectMultiple, ModelForm, ChoiceField, Form, MultipleChoiceField, ModelMultipleChoiceField, Select, TypedMultipleChoiceField, CheckboxSelectMultiple, TextInput
from experiment.models import ExperimentCollection, Experiment
from experiment.rules import EXPERIMENT_RULES

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


class ModelFormFieldAsJSON(ModelMultipleChoiceField):
    """ override clean method to prevent pk lookup to save querysets """
    def clean(self, value):
        return value


class MarkdownPreviewTextInput(TextInput):
    template_name = 'widgets/markdown_preview_text_input.html'


class ExperimentCollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['dashboard'].help_text = (
            'This field will be deprecated in the nearby future. '
            'Please use experiment series groups for dashboard configuration. (see bottom of form). <br><br>'
            'Legacy behavior: If you check "dashboard", the experiment collection will have a '
            'dashboard that shows all or a subgroup of related experiments along '
            'with a description, footer, and about page. If you leave it unchecked, '
            'the experiment collection will redirect to the first experiment.')
        self.fields['about_content'].widget = MarkdownPreviewTextInput()

    class Meta:
        model = ExperimentCollection
        fields = ['slug', 'description',
                  'dashboard', 'about_content']

    class Media:
        js = ["experiment_series_admin.js"]
        css = {"all": ["experiment_series_admin.css"]}


class ExperimentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        choices = tuple()
        for i in EXPERIMENT_RULES:
            choices += ((i, EXPERIMENT_RULES[i].__name__),)
        choices += (("", "---------"),)

        self.fields['rules'] = ChoiceField(
            choices=sorted(choices)
        )

        self.fields['questions'] = TypedMultipleChoiceField(
            choices=QUESTIONS_CHOICES,
            widget=CheckboxSelectMultiple,
            required=False
        )

    def clean_playlists(self):

        # Check if there is a rules id selected and key exists
        if 'rules' not in self.cleaned_data:
            return

        # Validat the rules' playlist
        rule_id = self.cleaned_data['rules']
        cl = EXPERIMENT_RULES[rule_id]
        rules = cl()

        playlists = self.cleaned_data['playlists']

        if not playlists:
            return self.cleaned_data['playlists']
        
        playlist_errors = []

        # Validate playlists
        for playlist in playlists:
            errors = rules.validate_playlist(playlist)

            for error in errors:
                playlist_errors.append(f"Playlist [{playlist.name}]: {error}")

        if playlist_errors:
            self.add_error('playlists', playlist_errors)

        return self.cleaned_data['playlists']

    class Meta:
        model = Experiment
        fields = ['name', 'slug', 'active', 'rules',
                  'rounds', 'bonus_points', 'playlists',]
        help_texts = {
            'description': 'A short description of the experiment that will be displayed on the experiment collection page and as a meta description in search engines.',
            'image': 'An image that will be displayed on the experiment collection page and as a meta image in search engines.',
            'consent': 'Upload an HTML (.html) or MARKDOWN (.md) file with a text to ask a user its consent<br> \
                      for using the experiment data for this instance of the experiment.<br> \
                      This field will override any consent text loaded from the rules file. <br>\
                      HTML files also allow django template tags so that the text can be translated',
            'slug': 'The slug is used to identify the experiment in the URL so you can access it on the web as follows: app.amsterdammusiclab.nl/{slug} <br>\
            It must be unique, lowercase and contain only letters, numbers, and hyphens. Nor can it start with any of the following reserved words: admin, server, experiment, participant, result, section, session, static.',
        }

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
