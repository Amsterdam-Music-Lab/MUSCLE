from django.db.models import Avg
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.questions.utils import question_by_key, total_unanswered_questions, unasked_question
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.goldsmiths import MSI_F1_ACTIVE_ENGAGEMENT

from experiment.actions import Consent, Explainer, Final, HTML, Playlist, Redirect, Step, StartSession, Trial
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, Form, LikertQuestionIcon
from experiment.actions.playback import Playback
from experiment.actions.styles import STYLE_BOOLEAN, STYLE_BOOLEAN_NEGATIVE_FIRST

from result.utils import prepare_result
from result.models import Result

from section.models import Section

from .base import Base
from .huang_2022 import gender_question, genre_question, get_test_playback, origin_question, residence_question


class MusicalPreferences(Base):
    ID = 'MUSICAL_PREFERENCES'
    preference_offset = 20
    knowledge_offset = 42

    questions = [
            question_by_key('msi_38_listen_music', MSI_F1_ACTIVE_ENGAGEMENT),
            genre_question(),
            gender_question(),
            question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
            origin_question(),
            residence_question()
        ]

    @classmethod
    def first_round(cls, experiment):
        explainer = Explainer(
            instruction=_('This experiment investigates musical preferences'),
            steps=[
                Step(description=_('Answer how much you like a song')),
                Step(description=_('Then tell us whether you know the song'))
            ],
            step_numbers=True,
        )
        consent = Consent()
        playlist = Playlist(experiment.playlists.all())
        start_session = StartSession()
        return [
            explainer,
            consent,
            playlist,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        next_round_number = session.get_current_round()
        if next_round_number == 1:
            playback = get_test_playback()
            html = HTML(body='<h4>{}</h4>'.format(_('Do you hear the music?')))
            form = Form(form=[BooleanQuestion(
                key='audio_check1',
                choices={'no': _('No'), 'yes': _('Yes')},
                result_id=prepare_result('audio_check1', session, 
                    scoring_rule='BOOLEAN'),
                submits=True,
                style=STYLE_BOOLEAN_NEGATIVE_FIRST)])
            return Trial(playback=playback, feedback_form=form, html=html,
                         config={'response_time': 15},
                         title=_("Audio check"))
        elif next_round_number <= 2:
            last_result = session.result_set.last()
            if last_result.question_key == 'audio_check1':
                if last_result.score == 0:
                    playback = get_test_playback()                    
                    html = HTML(body=render_to_string('html/huang_2022/audio_check.html'))
                    form = Form(form=[BooleanQuestion(
                        key='audio_check2',
                        choices={'no': _('Quit'), 'yes': _('Next')},
                        result_id=prepare_result('audio_check2', session, scoring_rule='BOOLEAN'),
                        submits=True,
                        style=STYLE_BOOLEAN_NEGATIVE_FIRST
                    )])
                    return Trial(playback=playback, html=html, feedback_form=form,
                                 config={'response_time': 15},
                                 title=_("Tech check"))
                else:
                    session.increment_round() # adjust round numbering
            elif last_result.question_key == 'audio_check2' and last_result.score == 0:
                # participant had persistent audio problems, delete session and redirect
                session.finish()
                session.save()
                return Redirect(settings.HOMEPAGE)
            
            question_trials = cls.get_questions(session)
            if question_trials:
                explainer = Explainer(
                    instruction=_("Questionnaire"),
                    steps=[
                        Step(_(
                            "To understand your musical preferences, we have 6 questions for you before the experiment \
                                begins. The first two questions are about your music listening experience, while the other \
                                four questions are demographic questions. It will take 2-3 minutes.")),
                        Step(_("Have fun!"))
                    ],
                    button_label=_("Let's go!")
                )
                return [explainer, *question_trials]

        elif next_round_number == 2:
            explainer = Explainer(
                instruction=_("How to play"),
                steps = [
                    Step(_("You will hear 64 music clips and have to answer two questions for each clip.")),
                    Step(_("It will take 20-30 minutes to complete the whole experiment.")),
                    Step(_("Either wear headphones or use your device's spekers.")),
                    Step(_("Your final results will be displayed at the end.")),
                    Step(_("Have fun!"))
                ],
                button_label=_("Start")
            )
            actions = [explainer]
        elif next_round_number == cls.preference_offset:
            like_results = session.result_set.filter(question_key='like_song')
            feedback = Trial(
                html=HTML(body=render_to_string('html/musical_preferences/feedback.html', {
                    'unlocked': _("Love"),
                    'n_songs': next_round_number,
                    'top_participant': cls.get_preferred_songs(like_results, 3)
                }))
            )
            actions = [feedback]
        elif next_round_number == cls.knowledge_offset:
            like_results = session.result_set.filter(question_key='like_song')
            known_songs = session.result_set.filter(question_key='know_song', score=2).count()
            feedback = Trial(
                html=HTML(body=render_to_string('html/musical_preferences/feedback.html', {
                    'unlocked': _("Knowledge"),
                    'n_songs': next_round_number,
                    'top_participant': cls.get_preferred_songs(like_results, 3),
                    'n_known_songs': known_songs
                }))
            )
            actions = [feedback]
        elif next_round_number == session.experiment.rounds:
            like_results = session.result_set.filter(question_key='like_song')
            known_songs = session.result_set.filter(question_key='know_song', score=2).count()
            all_results = Result.objects.filter(
                comment='like_song'
            )
            feedback = Trial(
                html=HTML(body=render_to_string('html/musical_preferences/feedback.html', {
                    'unlocked': _("Connection"),
                    'n_songs': next_round_number,
                    'top_participant': cls.get_preferred_songs(like_results, 3),
                    'n_known_songs': known_songs,
                    'top_all': cls.get_preferred_songs(all_results, 3)
                }))
            )
            actions = [feedback]

        
        section = session.playlist.random_section()
        like_key = 'like_song'
        likert = LikertQuestionIcon(
            question=_('How much do you like this song?'),
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
            result_id=prepare_result(know_key, session, section=section),
            style=STYLE_BOOLEAN
        )
        playback = Playback([section], play_config={'show_animation': True})
        form = Form([know, likert])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Musical preference'),
            config={
                'response_time': section.duration + .1,
            }
        )
        actions.append(view)
        return actions
    
    @classmethod
    def calculate_score(cls, result, data):
        result.comment = data.get('key')
        result.save()
        if data.get('key') == 'like_song':
            return int(data.get('value'))
        else:
            return None
    
    @classmethod
    def get_final_view(cls, session):
        # finalize experiment
        participant_results = session.result_set.filter(comment='like_song')
        participant_pref = cls.get_preferred_songs(participant_results)
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
        )
        return view
    
    @classmethod
    def get_preferred_songs(cls, result_set, n=5):
        top_songs = result_set.values('section').annotate(
            avg_score=Avg('score')).order_by()[:n]
        out_list = []
        for s in top_songs:
            section = Section.objects.get(pk=s.get('section'))
            out_list.append({'artist': section.song.artist, 'name': section.song.name})
        return out_list
    
    @classmethod
    def get_questions(cls, session):
        open_questions = total_unanswered_questions(session.participant, cls.questions)
        if not open_questions:
            return None
        trials = []
        for index in range(open_questions):
            question = unasked_question(session.participant, cls.questions)
            trials.append(Trial(
                title=_("Questionnaire %(index)i / %(total)i") % {'index': index+1, 'total': open_questions},
                feedback_form=Form([question])
            ))
        return trials

