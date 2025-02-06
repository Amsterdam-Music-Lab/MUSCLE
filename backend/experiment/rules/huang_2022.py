import logging

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings

from experiment.actions import HTML, Final, Explainer, Step, Redirect, Playlist, Trial
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.styles import ColorScheme
from question.questions import QUESTION_GROUPS
from result.utils import prepare_result
from session.models import Session
from .hooked import Hooked

logger = logging.getLogger(__name__)


class Huang2022(Hooked):
    """Rules for the Chinese version of the Hooked experiment."""

    ID = 'HUANG_2022'
    timeout = 15
    contact_email = 'musicexp_china@163.com'
    play_method = 'EXTERNAL'
    default_consent_file = 'consent/consent_huang2021.html'

    def __init__(self):
        self.question_series = [
            {
                "name": "MSI_ALL",
                "keys": QUESTION_GROUPS["MSI_ALL"],
                "randomize": False
            },
            {
                "name": "Demographics and other",
                "keys": [
                    'msi_39_best_instrument',
                    'dgf_genre_preference_zh',
                    'dgf_generation',
                    'dgf_education_huang_2022',
                    'dgf_highest_qualification_expectation',
                    'dgf_occupational_status',
                    'dgf_region_of_origin',
                    'dgf_region_of_residence',
                    'dgf_gender_identity_zh',
                    'contact'
                ],
                "randomize": False
            },
        ]

    def feedback_info(self):
        info = super().feedback_info()
        info['header'] = _("Any remarks or questions (optional):")
        info['thank_you'] = _("Thank you for your feedback!")
        return info

    def next_round(self, session: Session):
        """Get action data for the next round"""

        # If the number of results equals the number of block.rounds,
        # close the session and return data for the final_score view.
        json_data = session.json_data
        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        round_number = session.get_rounds_passed(self.counted_result_keys)
        total_rounds = session.block.rounds

        # Collect actions.
        actions = []
        plan = json_data.get('plan')

        if not plan:
            last_result = session.last_result()
            if not last_result:
                playback = get_test_playback()
                html = HTML(body='<h4>{}</h4>'.format(_('Do you hear the music?')))
                form = Form(
                    form=[
                        BooleanQuestion(
                            key='audio_check1',
                            choices={'no': _('No'), 'yes': _('Yes')},
                            result_id=prepare_result(
                                'audio_check1', session, scoring_rule='BOOLEAN'
                            ),
                            submits=True,
                            style=[ColorScheme.BOOLEAN_NEGATIVE_FIRST],
                        )
                    ]
                )
                return [Trial(playback=playback, feedback_form=form, html=html,
                             config={'response_time': 15},
                             title=_("Audio check"))]
            else:
                if last_result.score == 0:
                    # user indicated they couldn't hear the music
                    if last_result.question_key == 'audio_check1':
                        playback = get_test_playback()
                        html = HTML(body=render_to_string('html/huang_2022/audio_check.html'))
                        form = Form(
                            form=[
                                BooleanQuestion(
                                    key='audio_check2',
                                    choices={'no': _('Quit'), 'yes': _('Try')},
                                    result_id=prepare_result(
                                        'audio_check2', session, scoring_rule='BOOLEAN'
                                    ),
                                    submits=True,
                                    style=[ColorScheme.BOOLEAN_NEGATIVE_FIRST],
                                )
                            ]
                        )
                        return [Trial(playback=playback, html=html, feedback_form=form,
                                     config={'response_time': 15},
                                     title=_("Ready to experiment"))]
                    else:
                        # finish and redirect
                        session.finish()
                        session.save()
                        return Redirect(settings.HOMEPAGE)
                if last_result.score == 1:
                    # Start block: plan sections and show explainers
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
                    playlist = Playlist(session.block.playlists.all())
                    actions.extend([explainer, explainer_devices, playlist, *self.next_song_sync_action(session, round_number)])
        else:
            # Load the heard_before offset.
            heard_before_offset = session.json_data.get("heard_before_offset")

            # show score
            score = self.get_score(session, round_number)
            actions.append(score)

            # SongSync rounds
            if round_number < heard_before_offset:
                actions.extend(self.next_song_sync_action(session, round_number))
            # HeardBefore rounds
            elif round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(
                    self.next_heard_before_action(session, round_number))
            elif heard_before_offset < round_number < total_rounds:
                actions.append(
                    self.next_heard_before_action(session, round_number))
            else:
                questionnaire = self.get_open_questions(session)
                if questionnaire:
                    actions.extend([Explainer(
                        instruction=_("Please answer some questions \
                        on your musical (Goldsmiths-MSI) and demographic background"),
                        steps=[],
                        step_numbers=True,
                        button_label=_("Let's go!")), *questionnaire])
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
            json_data = result.json_data
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


def get_test_playback():
    from section.models import Section
    test_section = Section.objects.get(song__name='audiocheck')
    playback = Autoplay(
        sections=[test_section],
        show_animation=True
    )
    return playback
