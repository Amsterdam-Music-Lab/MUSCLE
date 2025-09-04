from django.conf import settings
from django.forms import (
    CheckboxSelectMultiple,
    ChoiceField,
    ModelForm,
    MultipleChoiceField,
)
from django.utils.translation import gettext_lazy as _

from experiment.models import (
    Block,
    SocialMediaConfig,
)
from experiment.rules import BLOCK_RULES


class BlockForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = tuple()
        for i in BLOCK_RULES:
            choices += ((i, BLOCK_RULES[i].__name__),)
        choices += (("", "---------"),)
        self.fields["rules"] = ChoiceField(choices=sorted(choices))

    def clean_playlists(self):
        # Check if there is a rulesid selected and key exists
        if "rules" not in self.cleaned_data:
            return self.cleaned_data["playlists"]

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
        fields = ["index", "slug", "name", "description",
                  "rounds", "bonus_points", "playlists", "rules", "theme_config"
                  ]
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


class SocialMediaConfigForm(ModelForm):
    channels = MultipleChoiceField(
        widget=CheckboxSelectMultiple, choices=SocialMediaConfig.SOCIAL_MEDIA_CHANNELS, required=False
    )

    class Meta:
        model = SocialMediaConfig
        fields = "__all__"
