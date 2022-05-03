
from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import Consent, Explainer, Step, Final, Playlist, StartSession, Trial
from .views.form import ChoiceQuestion, Form
from .views.playback import Playback
from .util.actions import combine_actions, final_action_with_optional_button


class ListeningConditions(Base):
    ID = 'LISTENING_CONDITIONS'

    @classmethod
    def next_round(cls, session, request_session=None):
        round_number = session.get_next_round()
        playback = None
        feedback_form = None
        if round_number == 1:
            feedback_form = Form([
                ChoiceQuestion(
                    key='quiet_room',
                    question=_(
                        "Are you in a quiet room?"),
                    choices={
                        'YES': _('YES'),
                        'MODERATELY': _('MODERATELY'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY',
                    submits=True
            )])
        elif round_number == 2:
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
            feedback_form = Form([
                ChoiceQuestion(
                    key='headphones',
                    question=_(
                        "Are you wearing headphones?"),
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY',
                    submits=True
                )
            ])
        elif round_number == 4:
            feedback_form = Form([
                ChoiceQuestion(
                    key='notifications_off',
                    question=_(
                        "Do you have sound notifications from other devices turned off?"),
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY',
                    submits=True
                ),
            ])
        elif round_number == 5:
            section = session.playlist.section_set.first()
            instruction = _("You can now set the sound to a comfortable level. \
                    You can then adjust the volume to as high a level as possible without it being uncomfortable. \
                    When you are satisfied with the sound level, click Continue")
            playback = Playback('AUTOPLAY', [section], instruction=instruction)
        view = Trial(playback, feedback_form)
        return view.action()


    @classmethod
    def first_round(cls, experiment):
        consent = Consent.action()
        explainer = Explainer(
            instruction=_(
                'General listening instructions:'),
            steps=[
                Step(_(
                        "To make sure that you can do the experiment as well as possible, please do it a quiet room with a stable internet connection."),
                ),
                Step(_("Please use headphones, and turn off sound notifications from other devices and applications (e.g., e-mail, phone messages)."),
                )],
            button_label=_('OK')
        ).action(True)
        playlist = Playlist.action(experiment.playlists.all())
        start_session = StartSession.action()
        return combine_actions(
            consent,
            explainer,
            playlist,
            start_session
        )
