import random

from django.utils.translation import gettext as _

from .base import BaseRules

from experiment.actions import Explainer, Step, Final, Trial
from experiment.actions.form import Form, RadiosQuestion
from experiment.actions.playback import Autoplay
from question.languages import LanguageQuestion

from session.models import Session

from result.utils import prepare_result


class Speech2Song(BaseRules):
    """ Rules for a speech-to-song experiment """
    ID = 'SPEECH_TO_SONG'
    default_consent_file = 'consent/consent_speech2song.html'

    n_presentations = 8
    n_trials_per_block = 8
    n_rounds_per_trial = 2

    def __init__(self):
        self.question_series = [
            {
                "name": "Question series Speech2Song",
                "keys": [
                    'dgf_age',
                    'dgf_gender_identity',
                    'dgf_country_of_origin_open',
                    'dgf_country_of_residence_open',
                    'lang_mother',
                    'lang_second',
                    'lang_third',
                    LanguageQuestion(_('English')).exposure_question().key,
                    LanguageQuestion(_('Brazilian Portuguese')).exposure_question().key,
                    LanguageQuestion(_('Mandarin Chinese')).exposure_question().key
                ],
                "randomize": False
            },
        ]

    def get_intro_explainer(self):
        return Explainer(
            instruction=_("This is an experiment about an auditory illusion."),
            steps=[
                Step(
                    description=_("Please wear headphones (earphones) during the experiment to maximise the experience of the illusion, if possible.")
                )
            ],
            button_label=_('Start')
        )

    def next_round(self, session: Session):
        blocks = [1, 2, 3]
        # shuffle blocks based on session.id as seed -> always same order for same session
        random.seed(session.id)
        random.shuffle(blocks)
        # group_ids for practice (0), or one of the speech blocks (1-3)
        actions = []
        is_speech = True
        rounds_passed = session.get_rounds_passed(self.counted_result_keys)
        if rounds_passed == 0:
            question_trials = self.get_open_questions(session)
            if question_trials:
                session.save_json_data({'quesionnaire': True})
                return [self.get_intro_explainer(), *question_trials]
            elif session.json_data.get("questionnaire"):
                explainer = Explainer(
                    instruction=_(
                        'Thank you for answering these questions about your background!'),
                    steps=[
                        Step(
                            description=_(
                                'Now you will hear a sound repeated multiple times.')
                        ),
                        Step(
                            description=_(
                                'Please listen to the following segment carefully, if possible with headphones.')
                        ),
                    ],
                    button_label=_('OK')
                )
                return [
                    explainer,
                    *self.next_repeated_representation(session, is_speech, 0)
                ]
            else:
                return [
                    self.get_intro_explainer(),
                    *self.next_repeated_representation(session, is_speech, 0)
                ]
        elif rounds_passed == 1:
            e1 = Explainer(
                instruction=_('Previous studies have shown that many people perceive the segment you just heard as song-like after repetition, but it is no problem if you do not share that perception because there is a wide range of individual differences.'),
                steps=[],
                button_label=_('Continue')
            )
            e2 = Explainer(
                instruction=_('Part 1'),
                steps=[
                    Step(
                        description=_('In the first part of the experiment, you will be presented with speech segments like the one just now in different languages which you may or may not speak.')),
                    Step(
                        description=_('Your task is to rate each segment on a scale from 1 to 5.'))
                ],
                button_label=_('Continue')
            )
            actions.extend([e1, e2])
            group_id = blocks[0]
        elif 2 <= rounds_passed <= self.n_trials_per_block * self.n_rounds_per_trial:
            group_id = blocks[0]
        elif self.n_trials_per_block * self.n_rounds_per_trial < rounds_passed <= 2 * self.n_trials_per_block * self.n_rounds_per_trial:
            group_id = blocks[1]
        elif 2 * self.n_trials_per_block * self.n_rounds_per_trial < rounds_passed <= 3 * self.n_trials_per_block * self.n_rounds_per_trial:
            group_id = blocks[2]
        elif rounds_passed == 3 * self.n_trials_per_block * self.n_rounds_per_trial + 1:
            # Final block (environmental sounds)
            e3 = Explainer(
                instruction=_('Part2'),
                steps=[
                    Step(
                        description=_(
                            'In the following part of the experiment, you will be presented with segments of environmental sounds as opposed to speech sounds.')
                    ),
                    Step(
                        description=_('Environmental sounds are sounds that are not speech nor music.')
                    ),
                    Step(
                        description=_('Like the speech segments, your task is to rate each segment on a scale from 1 to 5.')
                    )
                ],
                button_label=_('Continue')
            )
            actions.append(e3)
            group_id = 4
            is_speech = False
        elif 3 * self.n_trials_per_block * self.n_rounds_per_trial < rounds_passed <= 4 * self.n_trials_per_block * self.n_rounds_per_trial:
            group_id = 4
            is_speech = False
        else:
            # Finish session
            session.finish()
            session.save()
            # Return a score and final score action
            return Final(
                title=_('End of experiment'),
                session=session,
                final_text=_(
                    'Thank you for contributing your time to science!')
            )
        if rounds_passed % 2 == 1:
            # even round: single representation (first round are questions only)
            actions.extend(self.next_single_representation(
                session, is_speech, group_id))
        else:
            # uneven round: repeated representation
            actions.extend(self.next_repeated_representation(
                session, is_speech))
        return actions

    def next_single_representation(self, session: Session, is_speech: bool, group_id: int) -> list:
        """ combine a question after the first representation,
        and several repeated representations of the sound,
        with a final question"""
        filter_by = {'group': group_id}
        section = session.playlist.get_section(filter_by, song_ids=session.get_unused_song_ids())
        actions = [sound(section), self.speech_or_sound_question(session, section, is_speech)]
        return actions

    def next_repeated_representation(self, session: Session, is_speech: bool, group_id: int = -1) -> list:
        if group_id == 0:
            # for the Test case, there is no previous section to look at
            section = session.playlist.section_set.get(group=group_id)
        else:
            section = session.last_section()
        actions = [sound(section)] * self.n_presentations
        actions.append(self.speech_or_sound_question(session, section, is_speech))
        return actions

    def speech_or_sound_question(self, session, section, is_speech) -> Trial:
        if is_speech:
            question = question_speech(session, section)
        else:
            question = question_sound(session, section)
        return Trial(playback=None, feedback_form=Form([question]))


def question_speech(session, section):
    key = 'speech2song'
    return RadiosQuestion(
        key=key,
        question=_('Does this sound like song or speech to you?'),
        choices=[
            _('sounds exactly like speech'),
            _('sounds somewhat like speech'),
            _('sounds neither like speech nor like song'),
            _('sounds somewhat like song'),
            _('sounds exactly like song')],
        result_id=prepare_result(key, session, section=section, scoring_rule='LIKERT')
    )


def question_sound(session, section):
    key = 'sound2music'
    return RadiosQuestion(
        key=key,
        question=_(
            'Does this sound like music or an environmental sound to you?'),
        choices=[
            _('sounds exactly like an environmental sound'),
            _('sounds somewhat like an environmental sound'),
            _('sounds neither like an environmental sound nor like music'),
            _('sounds somewhat like music'),
            _('sounds exactly like music')],
        result_id=prepare_result(key, session, section=section, scoring_rule='LIKERT'),
    )


def sound(section):
    title = _('Listen carefully')
    playback = Autoplay(
        sections=[section],
    )
    view = Trial(
            playback=playback,
            feedback_form=None,
            title=title,
            config={
                'auto_advance': True,
                'show_continue_button': False,
                'response_time': section.duration+.5}
    )

    return view
