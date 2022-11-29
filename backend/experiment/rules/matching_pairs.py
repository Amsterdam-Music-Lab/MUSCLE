import random

from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import Consent, Explainer, Playlist, StartSession, Step, Trial
from .views.playback import Playback
from .views.form import Form

class MatchingPairs(Base):
    ID = 'MATCHING_PAIRS'

    @classmethod
    def first_round(cls, experiment):
        # 1. Explainer
        explainer = Explainer(
            instruction=_("How to Play"),
            steps=[
                Step(_(
                    "Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn.")),
                Step(_(
                    "Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!")),
                Step(_(
                    "Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"))
            ],
            button_label=_("Let's go!")).action(True)
        # 2. Consent
        consent = Consent.action()
        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            consent,
            playlist,
            start_session
        ]
    
    @staticmethod
    def next_round(session):
        sections = list(session.playlist.section_set.all())
        player_sections = random.sample(sections, 3)*2
        random.shuffle(player_sections)
        playback = Playback(
            sections=player_sections,
            player_type='MULTIPLAYER',
        )
        trial = Trial(
            title='Testing',
            playback=playback,
            feedback_form=None,
        )
        return trial.action()
    
    @classmethod
    def handle_result(cls, session, data):
        result = cls.get_result(session)
        result.json_data = data.get('json_data')
        result.score = data.get('decision_time')
        result.save()
