from django.db.models import Avg
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.questions.utils import question_by_key
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.goldsmiths import MSI_F1_ACTIVE_ENGAGEMENT

from experiment.actions import Consent, Explainer, Final, HTML, Playlist, Redirect, Step, StartSession, Trial
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, Form, LikertQuestionIcon
from experiment.actions.playback import Autoplay
from experiment.actions.styles import STYLE_BOOLEAN, STYLE_BOOLEAN_NEGATIVE_FIRST

from result.utils import prepare_result
from result.models import Result

from section.models import Section

from .base import Base
from .huang_2022 import gender_question, genre_question, get_test_playback, origin_question, residence_question


class MusicalPreferences(Base):
    ID = 'MUSICAL_PREFERENCES'
    consent_file = 'consent_musical_preferences.html'
    preference_offset = 20
    knowledge_offset = 42
    round_increment = 1

    know_score = {
        'yes': 2,
        'unsure': 1,
        'no': 0
    }

    def __init__(self):
        self.questions = [
            question_by_key('msi_38_listen_music', MSI_F1_ACTIVE_ENGAGEMENT),
            genre_question(),
            gender_question(),
            question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
            origin_question(),
            residence_question()
        ]

    def first_round(self, experiment):
        rendered = render_to_string('consent/{}'.format(self.consent_file)
        )
        consent = Consent(
            text=rendered, title=_('Informed consent'), confirm=_('I agree'), deny=_('Stop')
        )
        playlist = Playlist(experiment.playlists.all())
        explainer = Explainer(
            instruction=_('Welcome to the Musical Preferences experiment!'),
            steps=[
                Step(_('Please start by checking your connection quality.'))
            ],
            button_label=_('OK')
        )
        start_session = StartSession()
        return [
            consent,
            playlist,
            explainer,
            start_session
        ]

    def next_round(self, session, request_session=None):
        next_round_number = session.get_current_round()
        actions = []
        if next_round_number == 1:
            last_result = session.result_set.last()
            if last_result:
                if last_result.score == 1:
                    question_trials = self.get_questionnaire(session)
                    if question_trials:
                        n_questions = len(question_trials)
                        explainer = Explainer(
                            instruction=_("Questionnaire"),
                            steps=[
                                Step(_(
                                    "To understand your musical preferences, we have {} questions for you before the experiment \
                                        begins. The first two questions are about your music listening experience, while the other \
                                        four questions are demographic questions. It will take 2-3 minutes.").format(n_questions)),
                                Step(_("Have fun!"))
                            ],
                            button_label=_("Let's go!")
                        )
                        return [explainer, *question_trials]
                    else:
                        session.increment_round()
                        explainer = Explainer(
                            instruction=_("How to play"),
                            steps = [
                                Step(_("You will hear 64 music clips and have to answer two questions for each clip.")),
                                Step(_("It will take 20-30 minutes to complete the whole experiment.")),
                                Step(_("Either wear headphones or use your device's speakers.")),
                                Step(_("Your final results will be displayed at the end.")),
                                Step(_("Have fun!"))
                            ],
                            button_label=_("Start")
                        )
                        return [explainer]
                else:
                    session.decrement_round()
                    if last_result.question_key == 'audio_check1':
                        playback = get_test_playback('EXTERNAL')                    
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
                        # participant had persistent audio problems, delete session and redirect
                        session.finish()
                        session.save()
                        return Redirect(settings.HOMEPAGE)
            else:
                session.decrement_round()
                playback = get_test_playback('EXTERNAL')
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
        n_songs = next_round_number - self.round_increment
        if n_songs == self.preference_offset + 1:
            like_results = session.result_set.filter(question_key='like_song')
            feedback = Trial(
                html=HTML(body=render_to_string('html/musical_preferences/feedback.html', {
                    'unlocked': _("Love unlocked"),
                    'n_songs': n_songs - 1,
                    'top_participant': self.get_preferred_songs(like_results, 3)
                }))
            )
            actions = [feedback]
        elif n_songs == self.knowledge_offset + 1:
            like_results = session.result_set.filter(question_key='like_song')
            known_songs = session.result_set.filter(question_key='know_song', score=2).count()
            feedback = Trial(
                html=HTML(body=render_to_string('html/musical_preferences/feedback.html', {
                    'unlocked': _("Knowledge unlocked"),
                    'n_songs': n_songs - 1,
                    'top_participant': self.get_preferred_songs(like_results, 3),
                    'n_known_songs': known_songs
                }))
            )
            actions = [feedback]
        elif n_songs == session.experiment.rounds + 1:
            like_results = session.result_set.filter(question_key='like_song')
            known_songs = session.result_set.filter(question_key='know_song', score=2).count()
            all_results = Result.objects.filter(
                question_key='like_song'
            )
            top_participant = self.get_preferred_songs(like_results, 3)
            top_all = self.get_preferred_songs(all_results, 3)
            feedback = Trial(
                html=HTML(body=render_to_string('html/musical_preferences/feedback.html', {
                    'unlocked': _("Connection unlocked"),
                    'n_songs': n_songs - 1,
                    'top_participant': top_participant,
                    'n_known_songs': known_songs,
                    'top_all': top_all
                }))
            )
            session.finish()
            session.save()
            return [feedback, self.get_final_view(
                session,
                top_participant,
                known_songs,
                n_songs,
                top_all
            )]

        section = session.playlist.random_section()
        like_key = 'like_song'
        likert = LikertQuestionIcon(
            question=_('2. How much do you like this song?'),
            key=like_key,
            result_id=prepare_result(like_key, session, section=section, scoring_rule='LIKERT')
        )
        know_key = 'know_song'
        know = ChoiceQuestion(
            question=_('1. Do you know this song?'),
            key=know_key,
            view='BUTTON_ARRAY',
            choices={
                'yes': 'fa-check',
                'unsure': 'fa-question',
                'no': 'fa-xmark'                
            },
            result_id=prepare_result(know_key, session, section=section),
            style=STYLE_BOOLEAN
        )
        playback = Autoplay([section], show_animation=True)
        form = Form([know, likert])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Song %(round)s/%(total)s') %{
                'round': n_songs, 'total': session.experiment.rounds},
            config={
                'response_time': section.duration + .1,
            }
        )
        actions.append(view)
        return actions
    
    def calculate_score(self, result, data):
        if data.get('key') == 'know_song':
            return self.know_score.get(data.get('value'))
        else:
            return super().calculate_score(result, data)
    
    def social_media_info(self, experiment, top_participant, known_songs, n_songs, top_all):
        current_url =  "{}/{}".format(settings.RELOAD_PARTICIPANT_TARGET,
            experiment.slug
        )
        format_songs = lambda songs: ', '.join([song['name'] for song in songs])
        return {
            'apps': ['facebook', 'twitter'],
            'message': _("I explored musical preferences on %(url)s! My top 3 favorite songs: %(top_participant)s. I know %(known_songs)i out of %(n_songs)i songs. All players' top 3 songs: %(top_all)s") % {
                'url': current_url,
                'top_participant': format_songs(top_participant),
                'known_songs': known_songs,
                'n_songs': n_songs,
                'top_all': format_songs(top_all)
            },
            'url': experiment.url or current_url,
            'hashtags': [experiment.hashtag or experiment.slug, "amsterdammusiclab", "citizenscience"]
        }
    
    def get_final_view(self, session, top_participant, known_songs, n_songs, top_all):
        # finalize experiment
        social_info = self.social_media_info(
            session.experiment,
            top_participant,
            known_songs,
            n_songs,
            top_all
        )
        social_info['apps'] = ['weibo', 'share']
        view = Final(
            session,
            title=_("End"),
            final_text=_("Thank you for your participation and contribution to science!"),
            feedback_info=self.feedback_info(),
            social=social_info
        )
        return view
    
    def get_preferred_songs(self, result_set, n=5):
        top_songs = result_set.values('section').annotate(
            avg_score=Avg('score')).order_by()[:n]
        out_list = []
        for s in top_songs:
            section = Section.objects.get(pk=s.get('section'))
            out_list.append({'artist': section.song.artist, 'name': section.song.name})
        return out_list
