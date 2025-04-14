from django.conf import settings
from django.forms import (
    CheckboxSelectMultiple,
    ChoiceField,
    Form,
    ModelForm,
    ModelMultipleChoiceField,
    MultipleChoiceField,
    Select,
    TextInput,
)
from django.utils.translation import gettext_lazy as _

from experiment.models import (
    Experiment,
    Block,
    SocialMediaConfig,
)
from experiment.rules import BLOCK_RULES


# session_keys for Export CSV
SESSION_CHOICES = [
    ("block_id", "Block ID"),
    ("block_name", "Block name"),
    ("participant_id", "Participant ID"),
    ("participant_country", "Participant Country"),
    ("participant_access_info", "Participant access info"),
    ("session_start", "Session start time"),
    ("session_end", "Session end time"),
    ("final_score", "Final score"),
]

# result_keys for Export CSV
RESULT_CHOICES = [
    ("section_name", "Section name"),
    ("result_created_at", "Created time"),
    ("result_score", "Result score"),
    ("result_comment", "Result comment"),
    ("expected_response", "Expected response"),
    ("given_response", "Given response"),
    ("question_key", "Question key"),
]

# export_options for Export CSV
EXPORT_OPTIONS = [
    ("export_profile", "Include participants' profile Q&A"),
    ("session_data", "Include session data"),
    ("convert_session_json", "Convert session data JSON to CSV columns"),
    ("decision_time", "Include result decision time"),
    ("result_config", "Include result configuration parameters"),
    ("convert_result_json", "Convert result data JSON to CSV columns"),
    ("wide_format", "CSV wide format (Long format is default)"),
]

# Export templates for Export CSV
EXPORT_TEMPLATES = {
    "wide": [
        [
            "block_id",
            "block_name",
            "participant_id",
            "participant_country",
            "participant_access_info",
            "session_start",
            "session_end",
            "final_score",
        ],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        [
            "export_profile",
            "session_data",
            "convert_session_json",
            "decision_time",
            "result_config",
            "convert_result_json",
            "wide_format",
        ],
    ],
    "wide_json": [
        [
            "block_id",
            "block_name",
            "participant_id",
            "participant_country",
            "participant_access_info",
            "session_start",
            "session_end",
            "final_score",
        ],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        ["export_profile", "session_data", "decision_time", "result_config", "wide_format"],
    ],
    "wide_results": [
        ["block_name", "participant_id", "session_start", "session_end", "final_score"],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        ["session_data", "convert_session_json", "decision_time", "wide_format"],
    ],
    "wide_results_json": [
        ["block_name", "participant_id", "session_start", "session_end", "final_score"],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        ["session_data", "decision_time", "result_config", "wide_format"],
    ],
    "wide_profile": [
        ["block_name", "participant_id", "participant_country", "participant_access_info"],
        [],
        ["export_profile", "wide_format"],
    ],
    "long": [
        [
            "block_id",
            "block_name",
            "participant_id",
            "participant_country",
            "participant_access_info",
            "session_start",
            "session_end",
            "final_score",
        ],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        [
            "export_profile",
            "session_data",
            "convert_session_json",
            "decision_time",
            "result_config",
            "convert_result_json",
        ],
    ],
    "long_json": [
        [
            "block_id",
            "block_name",
            "participant_id",
            "participant_country",
            "participant_access_info",
            "session_start",
            "session_end",
            "final_score",
        ],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        ["export_profile", "session_data", "decision_time", "result_config"],
    ],
    "long_results": [
        ["block_name", "participant_id", "session_start", "session_end", "final_score"],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        ["session_data", "convert_session_json", "decision_time"],
    ],
    "long_results_json": [
        ["block_name", "participant_id", "session_start", "session_end", "final_score"],
        ["section_name", "result_created_at", "result_score", "result_comment", "expected_response", "given_response"],
        ["session_data", "decision_time", "result_config"],
    ],
    "long_profile": [
        ["block_name", "participant_id", "participant_country", "participant_access_info"],
        [],
        ["export_profile"],
    ],
}

# Export templates for Export CSV (ExportForm)
TEMPLATE_CHOICES = [
    ("wide", "CSV wide data format, All data"),
    ("wide_json", "CSV wide data format, All data, Keep JSON"),
    ("wide_results", "CSV wide data format, Session data, Results"),
    ("wide_results_json", "CSV wide data format, Session data as JSON, Results, Result data as JSON"),
    ("wide_profile", "CSV wide data format, Profile Q&A"),
    ("long", "CSV long data format, All data"),
    ("long_json", "CSV long data format, All data, Keep JSON"),
    ("long_results", "CSV long data format, Session data, Results"),
    ("long_results_json", "CSV long data format, Session data as JSON, Results, Result data as JSON"),
    ("long_profile", "CSV long data format, Profile Q&A"),
]


class ModelFormFieldAsJSON(ModelMultipleChoiceField):
    """override clean method to prevent pk lookup to save querysets"""

    def clean(self, value):
        return value


class MarkdownPreviewTextInput(TextInput):
    template_name = "widgets/markdown_preview_text_input.html"

    class Media:
        css = {"all": ["markdown_preview.css"]}
        js = ["markdown_preview.js"]


class ExperimentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for language in settings.MODELTRANSLATION_LANGUAGES:
            language = language.replace('-', '_')
            desc_field = f"description_{language}"
            self.fields[desc_field].widget.attrs["style"] = "height:40px"
            soc_field = f"social_media_message_{language}"
            self.fields[soc_field].widget.attrs["style"] = "height:15px"

    class Meta:
        model = Experiment
        fields = "__all__"
        help_texts = {}
        for language in settings.MODELTRANSLATION_LANGUAGES:
            for field_name in ["about_content", "disclaimer", "privacy"]:
                language = language.replace("-", "_")
                lang_field_name = f"{field_name}_{language}"
                help_texts.update(
                    {
                        lang_field_name: _(
                            "You can enter plain text, html or markdown here."
                        )
                    }
                )

    class Media:
        js = ["experiment_form.js"]
        css = {"all": ["experiment_form.css"]}


class BlockForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        choices = tuple()
        for i in BLOCK_RULES:
            choices += ((i, BLOCK_RULES[i].__name__),)
        choices += (("", "---------"),)

        self.fields["rules"] = ChoiceField(choices=sorted(choices))

    def clean_playlists(self):
        # Check if there is a rules id selected and key exists
        if "rules" not in self.cleaned_data:
            return

        # Validat the rules' playlist
        rule_id = self.cleaned_data["rules"]
        cl = BLOCK_RULES[rule_id]
        rules = cl()

        playlists = self.cleaned_data["playlists"]

        if not playlists:
            return self.cleaned_data["playlists"]

        playlist_errors = []

        # Validate playlists
        for playlist in playlists:
            errors = rules.validate_playlist(playlist)

            for error in errors:
                playlist_errors.append(f"Playlist [{playlist.name}]: {error}")

        if playlist_errors:
            self.add_error("playlists", playlist_errors)

        return playlists

    class Meta:
        model = Block
        fields = "__all__"
        help_texts = {
            "name": _("The name and description will be displayed in dashboard mode."),
            "image": _(
                "An image that will be displayed on the experiment page and as a meta image in search engines."
            ),
            "slug": _(
                "The slug is used to identify the block in the URL so you can access it on the web as follows: app.amsterdammusiclab.nl/{slug} <br>\
            It must be unique, lowercase and contain only letters, numbers, and hyphens. Nor can it start with any of the following reserved words: admin, server, block, participant, result, section, session, static."
            ),
        }


class ExportForm(Form):
    export_session_fields = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=SESSION_CHOICES)
    export_result_fields = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=RESULT_CHOICES)
    export_options = MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=EXPORT_OPTIONS,
    )


class TemplateForm(Form):
    select_template = ChoiceField(widget=Select, choices=TEMPLATE_CHOICES)


class SocialMediaConfigForm(ModelForm):
    channels = MultipleChoiceField(
        widget=CheckboxSelectMultiple, choices=SocialMediaConfig.SOCIAL_MEDIA_CHANNELS, required=False
    )

    class Meta:
        model = SocialMediaConfig
        fields = "__all__"
