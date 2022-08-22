from django.utils.translation import gettext_lazy as _

from .views import Trial, Consent, Explainer, Playlist, Step, StartSession
from .views.form import ChoiceQuestion, Form, LikertQuestion
from .views.playback import Playback

from .base import Base

class MusicalPreferences(Base):
    ID = 'MUSICAL_PREFERENCES'

    @classmethod
    def first_round(cls, experiment):
        explainer = Explainer(
            instruction=_('This experiment investigates musical preferences'),
            steps=[
                Step(description=_('Answer how much you like a song')),
                Step(description=_('Then tell us whether you know the song'))
            ]
        ).action(True)
        consent = Consent.action()
        playlist = Playlist.action(experiment.playlists.all())
        start_session = StartSession.action()
        return [
            explainer,
            consent,
            playlist,
            start_session
        ]

    @classmethod
    def next_round(cls, session):
        section = session.playlist.random_section()
        likert = LikertQuestion(
            question=_('Do you like this song?'),
            key='like_song'
        )
        know = ChoiceQuestion(
            question=_('Do you know this song?'),
            key='know_song',
            view='BUTTON_ARRAY',
            choices={
                'yes': '👌',
                'no': '🙅',
                'unsure': '😕'
            }
        )
        playback = Playback([section], play_config={'show_animation': True})
        form = Form([likert, know])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Musical preference'),
            config={
                'decision_time': section.duration + .1
            }
        )
        return view.action()

