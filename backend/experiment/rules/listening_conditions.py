
from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import CompositeView, Consent, Explainer, Final, Playlist, StartSession
from .views.players import Player, Players
from .views.form import ChoiceQuestion, Form
from .util.actions import combine_actions


class ListeningConditions(Base):
    ID = 'LISTENING_CONDITIONS'

    @classmethod
    def next_round(cls, session):
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
                    view='BUTTON_ARRAY'
                ),
                ChoiceQuestion(
                    key='internet_connection',
                    question=_(
                        "Do you have a stable internet connection?"),
                    choices={
                        'YES': _('YES'),
                        'MODERATELY': _('MODERATELY'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY'
                ),
                ChoiceQuestion(
                    key='headphones',
                    question=_(
                        "Are you wearing headphones?"),
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY'
                ),
                ChoiceQuestion(
                    key='notifications_off',
                    question=_(
                        "Do you have sound notifications from other devices turned off?"),
                    choices={
                        'YES': _('YES'),
                        'NO': _('NO')
                    },
                    view='BUTTON_ARRAY'
                ),
            ])
            view = CompositeView(None, feedback_form.action())
            return view.action()
        elif round_number==2:
            section = session.playlist.section_set.first()
            instructions = {
                'during_presentation': _("You can now set the sound to a comfortable level. \
                    When you click the button below, you will hear a sound. \
                    You can then adjust the volume to as high a level as possible without it being uncomfortable. \
                    Please keep the eventual sound level the same over the course of the experiment."),
            }
            feedback_form = None
            player = Player(section,'SMALL_PLAYER')
            players = Players([player])
            view = CompositeView(players.action(), feedback_form, instructions)
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