from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions.utils import combine_actions
from experiment.questions.utils import question_by_key

from experiment.actions import Consent, Explainer, Final, Playlist, Step, StartSession, Trial
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, Form, LikertQuestionIcon
from experiment.actions.playback import Playback

from result.utils import prepare_result

from .base import Base


class MusicalPreferences(Base):
    ID = 'MUSICAL_PREFERENCES'
    block_size = 16

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
        if session.last_result() and session.last_result().score == -1:
            # last result was key='continue', value='no':
            return cls.get_final_view(session)
        n_results = session.rounds_passed()
        if (n_results > 0 and int(n_results / 2) % cls.block_size == 0):
            # end of a block
            actions = []
            if int(n_results / 2) == session.experiment.rounds:
                return cls.get_final_view(session)
            elif int(n_results / 2) == cls.block_size:
                # first time we hit the end of a block, present questionnaire
                actions.append(Explainer(
                    instruction=_("Please answer some questions \
                    on your musical (Goldsmiths-MSI) and demographic background"),
                    steps=[],
                    button_label=_("Let's go!")).action()
                )
                actions.extend(cls.get_questions(session))
            question = BooleanQuestion(
                question=_("Would you like to listen to more songs?"),
                choices={
                    'yes': 'fa-thumbs-up',
                    'no': 'fa-thumbs-down'
                },
                key='continue',
                submits=True
            )
            actions.append(
                Trial(
                    feedback_form=Form([question]),
                    config={'style': 'boolean'}
                ).action()
            )
            return combine_actions(*actions)

        section = session.playlist.random_section()
        like_key = 'like_song'
        likert = LikertQuestionIcon(
            question=_('Do you like this song?'),
            key=like_key,
            result_id=prepare_result(like_key, session, section=section, scoring_rule='LIKERT')
        )
        know_key = 'know_song'
        know = ChoiceQuestion(
            question=_('Do you know this song?'),
            key=know_key,
            view='BUTTON_ARRAY',
            choices={
                'no': 'fa-thumbs-down',
                'unsure': 'fa-question',
                'yes': 'fa-thumbs-up',
            },
            result_id=prepare_result(know_key, session, section=section)
        )
        playback = Playback([section], play_config={'show_animation': True})
        form = Form([likert, know])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Musical preference'),
            config={
                'response_time': section.duration + .1,
                'style': 'boolean'
            }
        )
        return view.action()
    
    @classmethod
    def calculate_score(cls, result, data):
        result.comment = data.get('key')
        result.save()
        if data.get('key') == 'like_song':
            return int(data.get('value'))
        elif data.get('key') == 'continue':
            if data.get('value') == 'no':
                return -1
        else:
            return None
    
    @classmethod
    def get_final_view(cls, session):
        # finalize experiment
        participant_results = session.result_set.filter(comment='like_song')
        participant_pref = cls.get_preferred_songs(participant_results)
        from experiment.models.result import Result 
        all_results = Result.objects.filter(
            comment='like_song'
        )
        all_pref = cls.get_preferred_songs(all_results)
        feedback = render_to_string('final/musical_preferences.html', 
        {'top_all': all_pref, 'top_participant': participant_pref})
        view = Final(
            session,
            title='Preference overview',
            final_text=feedback,
            show_social=True
        ).action()
        return view
    
    @classmethod
    def get_preferred_songs(cls, result_set, n=5):
        top_songs = result_set.values('section').annotate(
            avg_score=Avg('score')).order_by()[:n]
        from section.models import Section
        out_list = []
        for s in top_songs:
            section = Section.objects.get(pk=s.get('section'))
            out_list.append({'name': section.name, 'score': s.get('avg_score')})
        return out_list
    
    @classmethod
    def get_questions(cls, session):
        questions = [
            question_by_key('dgf_generation'),
            question_by_key('dgf_education', drop_choices=['isced-5']),
        ]
        return [
            Trial(
                title=_("Questionnaire"),
                feedback_form=Form([question])).action() 
            for question in questions
        ]

