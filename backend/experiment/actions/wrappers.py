import random

from django.utils.translation import gettext as _

from .form import BooleanQuestion, ChoiceQuestion, Form
from .playback import Autoplay, PlayButton
from .trial import Trial

from experiment.actions.utils import randomize_playhead
from result.utils import prepare_result
from section.models import Section
from session.models import Session


def two_alternative_forced(session, section, choices, expected_response=None, style={}, comment='', scoring_rule=None, title='', config=None):
    """
    Provide data for a Two Alternative Forced view that (auto)plays a section,
    shows a question and has two customizable buttons
    """
    playback = PlayButton(
        [section]
    )
    key = 'choice'
    button_style = {'invisible-text': True,
                    'buttons-large-gap': True, 'buttons-large-text': True}
    button_style.update(style)
    question = ChoiceQuestion(
        key=key,
        result_id=prepare_result(
            key,
            session=session,
            section=section,
            expected_response=expected_response,
            scoring_rule=scoring_rule,
            comment=comment
        ),
        choices=choices,
        view='BUTTON_ARRAY',
        submits=True,
        style=button_style
    )
    feedback_form = Form([question])
    trial = Trial(playback=playback, feedback_form=feedback_form,
                  title=title, config=config)
    return trial


def song_sync(session: Session, section: Section, title: str,
              recognition_time=15, sync_time=15,
              min_jitter=10, max_jitter=15):
    trial_config = {
        'response_time': recognition_time,
        'auto_advance': True
    }
    recognize = Trial(
        feedback_form=Form([BooleanQuestion(
            key='recognize',
            result_id=prepare_result(
                'recognize', session, section=section, scoring_rule='SONG_SYNC_RECOGNITION'),
            submits=True
        )]),
        playback=Autoplay([section], show_animation=True,
                          preload_message=_('Get ready!'),
                          instruction=_('Do you recognize the song?'),
                          ),
        config={**trial_config,
                'break_round_on': {'EQUALS': ['TIMEOUT', 'no']}},
        title=title
    )
    silence_time = 4
    silence = Trial(
        playback=Autoplay([section],
                          show_animation=True,
                          instruction=_('Keep imagining the music'),
                          mute=True),
        config={
            'response_time': silence_time,
            'auto_advance': True,
            'show_continue_button': False,
        },
        title=title
    )
    continuation_correctness = random.choice([True, False])
    jitter = randomize_playhead(min_jitter, max_jitter, continuation_correctness)
    trial_config['response_time'] = sync_time
    correct_place = Trial(
        feedback_form=Form(
            [
                BooleanQuestion(
                    key="correct_place",
                    submits=True,
                    result_id=prepare_result(
                        "correct_place",
                        session,
                        section=section,
                        scoring_rule="SONG_SYNC_CONTINUATION",
                        json_data={"continuation_offset": jitter},
                        expected_response="yes" if continuation_correctness else "no",
                    ),
                )
            ]
        ),
        playback=Autoplay(
            [section],
            instruction=_("Did the track come back in the right place?"),
            show_animation=True,
            play_from=silence_time + jitter,
            resume_play=True,
        ),
        config=trial_config,
        title=title,
    )
    return [recognize, silence, correct_place]
