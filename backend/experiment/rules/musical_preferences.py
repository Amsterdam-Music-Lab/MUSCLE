from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from .views import Trial, Consent, Explainer, Playlist, Step, StartSession, Score
from .views.form import ChoiceQuestion, Form, LikertQuestion
from .views.playback import Playback

from .base import Base

class MusicalPreferences(Base):
    ID = 'MUSICAL_PREFERENCES'
    n_rounds = 8

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
    def next_round(cls, session, request_session=None):
        round_number = session.get_next_round()
        if round_number == cls.n_rounds:
            participant_results = session.result_set.filter(comment='like_song')
            participant_pref = cls.get_preferred_songs(participant_results)
            all_results = []
            for s in session.experiment.session_set.all():
                if s.experiment.rules==cls.ID:
                    all_results.extend(s.result_set.filter(comment='like_song'))
            all_pref = cls.get_preferred_songs(all_results)
            view = Score(
                session,
                feedback = participant_pref
            ).action()


        section = session.playlist.random_section()
        result_id = cls.prepare_result(session, section)
        likert = LikertQuestion(
            question=_('Do you like this song?'),
            key='like_song',
            result_id=result_id
        )
        result_id = cls.prepare_result(session, section)
        know = ChoiceQuestion(
            question=_('Do you know this song?'),
            key='know_song',
            result_id=result_id,
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
    
    @classmethod
    def calculate_score(cls, result, data, form_element):
        result.comment = form_element.get('key')
        result.save()
        if form_element.get('key') == 'like_song':
            return int(form_element.get('value'))
        else:
            return None
    
    @classmethod
    def get_preferred_songs(result_set, n=5):
        top_songs = result_set.values('section').annotate(
            avg_score=Avg('score')).order_by()[:n]
        from experiment.models.section import Section
        out_list = []
        for s in top_songs:
            section = Section.objects.get(pk=s.section)
            out_list.append({'artist': section.artist, 'name': section.name})
        return out_list

