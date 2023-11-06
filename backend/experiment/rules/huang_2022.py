import logging

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings

from experiment.actions import HTML, Final, Score, Explainer, Step, Consent, StartSession, Redirect, Playlist, Trial
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, Form, Question
from experiment.actions.playback import Autoplay
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.goldsmiths import MSI_ALL
from experiment.questions.utils import question_by_key
from experiment.actions.styles import STYLE_BOOLEAN_NEGATIVE_FIRST
from result.utils import prepare_result
from .hooked import Hooked

logger = logging.getLogger(__name__)

region_choices = {
    'HD': '华东（山东、江苏、安徽、浙江、福建、江西、上海）',
    'HN': '华南（广东、广西、海南）',
    'HZ': '华中（湖北、湖南、河南、江西）',
    'HB': '华北（北京、天津、河北、山西、内蒙古）',
    'XB': '西北（宁夏、新疆、青海、陕西、甘肃）',
    'XN': '西南（四川、云南、贵州、西藏、重庆）',
    'DB': '东北（辽宁、吉林、黑龙江）',
    'GAT': '港澳台（香港、澳门、台湾）',
    'QT': '国外',
    'no_answer': '不想回答'
}


def origin_question():
    return ChoiceQuestion(
        key='dgf_region_of_origin',
        view='DROPDOWN',
        question=_(
            "In which region did you spend the most formative years of your childhood and youth?"),
        choices=region_choices,
    )


def residence_question():
    return ChoiceQuestion(
        view='DROPDOWN',
        key='dgf_region_of_residence',
        question=_("In which region do you currently reside?"),
        choices=region_choices,
    )


def gender_question():
    return ChoiceQuestion(
        key='dgf_gender_identity',
        view='RADIOS',
        question="您目前对自己的性别认识?",
        choices={
            'male': "男",
            'Female': "女",
            'Others': "其他",
            'no_answer': "不想回答"
        }
    )

def genre_question():
    return ChoiceQuestion(
        view='DROPDOWN',
        key='dgf_genre_preference',
        question=_(
            "To which group of musical genres do you currently listen most?"),
        choices={
            'unpretentious': _("Pop/Country/Religious"),
            'Chinese artistic': _("Folk/Mountain songs"),
            'sophisticated': _("Western classical music/Jazz/Opera/Musical"),
            'classical': _("Chinese opera"),
            'intense': _("Rock/Punk/Metal"),
            'mellow': _("Dance/Electronic/New Age"),
            'contemporary': _("Hip-hop/R&B/Funk"),
        }
    )

def contact_question():
    return Question(
            key='contact',
            explainer=_(
                "Thank you so much for your feedback! Feel free to include your contact information if you would like a reply or skip if you wish to remain anonymous."
            ),
            question=_(
                "Contact (optional):"
            ),
            is_skippable=True
        )

class Huang2022(Hooked):
    """Rules for the Chinese version of the Hooked experiment."""

    ID = 'HUANG_2022'
    timeout = 15
    round_modifier = 2
    contact_email = 'musicexp_china@163.com'
    play_method = 'EXTERNAL'

    def __init__(self):
        self.questions = MSI_ALL + [
            question_by_key('msi_39_best_instrument'),
            genre_question(),
            question_by_key('dgf_generation'),
            question_by_key('dgf_education', drop_choices=['isced-5']),
            question_by_key(
                'dgf_highest_qualification_expectation', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_occupational_status', EXTRA_DEMOGRAPHICS),
            origin_question(),
            residence_question(),
            gender_question(),
            contact_question()
        ]

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""
        # read consent form from file
        rendered = render_to_string(
            'consent/consent_huang2021.html')
        consent = Consent(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        playlist = Playlist(experiment.playlists.all())
        # start session
        start_session = StartSession()

        return [
            consent,
            playlist,
            start_session
        ]

    def feedback_info(self):
        info = super().feedback_info()
        info['header'] = _("Any remarks or questions (optional):")
        info['thank_you'] = _("Thank you for your feedback!")
        return info
    
    def next_round(self, session):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        json_data = session.load_json_data()
        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_current_round() - self.round_modifier 
        total_rounds = session.experiment.rounds

        # Collect actions.
        actions = []

        if next_round_number == -1:
            playback = get_test_playback(self.play_method)
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
        elif next_round_number <= 1:
            last_result = session.result_set.last()
            if last_result.question_key == 'audio_check1':
                if last_result.score == 0:
                    playback = get_test_playback(self.play_method)
                    html = HTML(body=render_to_string('html/huang_2022/audio_check.html'))
                    form = Form(form=[BooleanQuestion(
                        key='audio_check2',
                        choices={'no': _('Quit'), 'yes': _('Try')},
                        result_id=prepare_result('audio_check2', session, scoring_rule='BOOLEAN'),
                        submits=True,
                        style=STYLE_BOOLEAN_NEGATIVE_FIRST
                    )])
                    return Trial(playback=playback, html=html, feedback_form=form,
                                 config={'response_time': 15},
                                 title=_("Ready to experiment"))
                else:
                    session.increment_round() # adjust round numbering
            elif last_result.question_key == 'audio_check2' and last_result.score == 0:
                # participant had persistent audio problems, delete session and redirect
                session.finish()
                session.save()
                return Redirect(settings.HOMEPAGE)

            # Start experiment: plan sections and show explainers
            self.plan_sections(session)
            # Show explainers and go to SongSync
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
            step_numbers=True,
            button_label=_("Let's go!"))
            explainer_devices = Explainer(
                instruction=_("You can use your smartphone, computer or tablet to participate in this experiment. Please choose the best network in your area to participate in the experiment, such as wireless network (WIFI), mobile data network signal (4G or above) or wired network. If the network is poor, it may cause the music to fail to load or the experiment may fail to run properly. You can access the experiment page through the following channels:"),
                steps=[
                    Step(_(
                        "Directly click the link on WeChat (smart phone or PC version, or WeChat Web)"),
                    ),
                    Step(_(
                        "If the link to load the experiment page through the WeChat app on your cell phone fails, you can copy and paste the link in the browser of your cell phone or computer to participate in the experiment. You can use any of the currently available browsers, such as Safari, Firefox, 360, Google Chrome, Quark, etc."),
                    )
                ],
                step_numbers=True,
                button_label=_("Continue")
            )
            # Choose playlist
            actions.extend([explainer, explainer_devices, self.next_song_sync_action(session)])
        else:
            # Load the heard_before offset.
            plan = json_data.get('plan')
            heard_before_offset = len(plan['song_sync_sections']) + 1

            # show score 
            config = {'show_section': True, 'show_total_score': True}
            title = self.get_trial_title(session, next_round_number - 1)
            score = Score(
                session,
                config=config,
                title=title
            )
            actions.append(score)
            
            # SongSync rounds
            if next_round_number < heard_before_offset:
                actions.append(self.next_song_sync_action(session))
            # HeardBefore rounds
            elif next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(
                    self.next_heard_before_action(session))
            elif heard_before_offset < next_round_number <= total_rounds:
                actions.append(
                    self.next_heard_before_action(session))   
            elif next_round_number == total_rounds + 1:
                questionnaire = self.get_questionnaire(session)
                if questionnaire:
                    actions.extend([Explainer(
                        instruction=_("Please answer some questions \
                        on your musical (Goldsmiths-MSI) and demographic background"),
                        steps=[],
                        step_numbers=True,
                        button_label=_("Let's go!")), *questionnaire])
                    session.increment_round()
                else:
                    actions.append(self.finalize(session))
            else:
                return [self.finalize(session)]
        return actions
    
    def finalize(self, session):
        session.finish()
        session.save()
        return Final(
            session=session,
            final_text=self.final_score_message(session),
            rank=self.rank(session),
            show_profile_link=True,
            feedback_info=self.feedback_info()
        )
    
    def final_score_message(self, session):
        """Create final score message for given session"""

        n_sync_guessed = 0
        sync_time = 0
        n_sync_correct = 0
        n_old_new_expected = 0
        n_old_new_correct = 0

        for result in session.result_set.all():
            json_data = result.load_json_data()
            if json_data.get('result') and json_data['result']['type'] == 'recognized':
                n_sync_guessed += 1
                sync_time += json_data['result']['recognition_time']
                if result.score > 0:
                    n_sync_correct += 1
            else:
                if result.expected_response == 'old':
                    n_old_new_expected += 1
                    if result.score > 0:
                        n_old_new_correct += 1
        thanks_message = _("Thank you for your contribution to science!")
        score_message = _(
            "Well done!") if session.final_score > 0 else _("Too bad!")
        if n_sync_guessed == 0:
            song_sync_message = _("You did not recognise any songs at first.")
        else:
            song_sync_message = _("It took you %(n_seconds)d s to recognise a song on average, \
                and you correctly identified %(n_correct)d out of the %(n_total)d songs you thought you knew.") % {
                'n_seconds': round(sync_time / n_sync_guessed, 1),
                'n_correct': n_sync_correct,
                'n_total': n_sync_guessed
            }
        heard_before_message = _("During the bonus rounds, you remembered %(n_correct)d of the %(n_total)d songs that came back.") % {
            'n_correct': n_old_new_correct,
            'n_total': n_old_new_expected
        }
        messages = [
            thanks_message, score_message, song_sync_message, heard_before_message
        ]
        return " ".join([str(m) for m in messages])

def get_test_playback(play_method):
    from section.models import Section
    test_section = Section.objects.get(song__name='audiocheck')
    playback = Autoplay(
        sections=[test_section],
        show_animation=True
    )
    return playback
    