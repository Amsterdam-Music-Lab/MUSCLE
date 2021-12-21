
from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import CompositeView, Consent, Explainer, Final, Playlist, StartSession
from .views.form import ChoiceQuestion, Form
from .util.actions import final_action_with_optional_button


class ListeningConditions(Base):
    ID = 'LISTENING_CONDITIONS'

    @classmethod
    def next_round(cls, session, request_session=None):
        round_number = session.get_next_round()
        if round_number == 1:
            feedback_form = Form([
                ChoiceQuestion(
                    key='quiet_room',
                    question=_(
                        "Are you in a quiet room?"),
                    choices={
                        'YES': _('YES'),
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
            instructions = {
                'preload': "",
                'during_presentation': _("You can now set the sound to a comfortable level. \
                    You can then adjust the volume to as high a level as possible without it being uncomfortable. \
                    When you are satisfied with the sound level, click Continue"),
            }
            feedback_form = Form([])
            view = CompositeView(section, feedback_form.action(), instructions)
            return view.action()
        else:
            message = _("Please keep the eventual sound level the same over the course of the experiment.")
            return final_action_with_optional_button(session, message, request_session)
        view = CompositeView(None, feedback_form.action())
        return view.action()
        
    @classmethod
    def first_round(cls, experiment):
        consent = Consent.action()
        playlist = Playlist.action(experiment.playlists.all())
        start_session = StartSession.action()
        return combine_actions(
            consent,
            playlist,
            start_session
        )