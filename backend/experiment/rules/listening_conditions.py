
from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Consent, Explainer, Step, Playlist, Trial
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.utils import final_action_with_optional_button
from result.utils import prepare_result


class ListeningConditions(Base):
    ID = 'LISTENING_CONDITIONS'

    def next_round(self, session, request_session=None):
        round_number = session.get_next_round()
        playback = None
        feedback_form = None
        if round_number == 1:
            key = 'quiet_room'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form([
                ChoiceQuestion(
                    key=key,
                    question=_(
                        "Are you in a quiet room?"),
                    choices={
                        'YES': _('YES'),
                        'MODERATELY': _('MODERATELY'),
                        'NO': _('NO')
                    },
                    result_id=result_pk,
                    view='BUTTON_ARRAY',
                    submits=True
                )])
        elif round_number == 2:
            key = 'internet_connection'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form([ChoiceQuestion(
                key='internet_connection',
                question=_(
                    "Do you have a stable internet connection?"),
                choices={
                    'YES': _('YES'),
                    'MODERATELY': _('MODERATELY'),
                    'NO': _('NO')
                },
                view='BUTTON_ARRAY',
                submits=True
            )])
        elif round_number == 3:
            key = 'headphones'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form([
                ChoiceQuestion(
                    key=key,
                    question=_(
                        "Are you wearing headphones?"),
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY',
                    result_id=result_pk,
                    submits=True
                )
            ])
        elif round_number == 4:
            key = 'notifications_off'
            result_pk = prepare_result(key, session, expected_response=key)
            feedback_form = Form([
                ChoiceQuestion(
                    key=key,
                    question=_(
                        "Do you have sound notifications from other devices turned off?"),
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY',
                    result_id=result_pk,
                    submits=True
                ),
            ])
        elif round_number == 5:
            section = session.playlist.section_set.first()
            instruction = _("You can now set the sound to a comfortable level. \
                    You can then adjust the volume to as high a level as possible without it being uncomfortable. \
                    When you are satisfied with the sound level, click Continue")
            playback = Autoplay([section], instruction=instruction)
            message = _(
                "Please keep the eventual sound level the same over the course of the experiment.")
            actions = [
                Trial(playback, feedback_form),
                final_action_with_optional_button(
                    session, message, request_session)
            ]
            return actions

        view = Trial(playback, feedback_form=feedback_form)

        return [view]

    def first_round(self, experiment):
        # Consent with admin text or default text
        consent = Consent(experiment.consent)
        explainer = Explainer(
            instruction=_(
                'General listening instructions:'),
            steps=[
                Step(_(
                    "To make sure that you can do the experiment as well as possible, please do it a quiet room with a stable internet connection."),
                ),
                Step(_("Please use headphones, and turn off sound notifications from other devices and applications (e.g., e-mail, phone messages)."),
                     )],
            step_numbers=True,
            button_label=_('OK')
        )
        playlist = Playlist(experiment.playlists.all())
        return [
            consent,
            explainer,
            playlist,
        ]
