import numpy as np
import sys
from os.path import isdir

from django.utils.translation import gettext as _
from django.template.loader import render_to_string

from .base import Base

from .views import Consent, Explainer, Final, Question, Playlist, CompositeView, StartSession
from .util.actions import combine_actions
from .util.questions import question_by_key, EXTRA_DEMOGRAPHICS
from .util.languages import LANGUAGE, LanguageQuestion

n_representations = 8
n_trials_per_block = 8
n_rounds_per_block = n_trials_per_block * 2  # each trial has two rounds


class Speech2Song(Base):
    """ Rules for a speech-to-song experiment """
    ID = 'SPEECH_TO_SONG'

    @staticmethod
    def first_round(experiment):
        explainer = Explainer.action(
            instruction=_("This is an experiment about an auditory illusion."),
            steps=[
                Explainer.step(
                    description=_("Please wear headphones (earphones) during the experiment to maximise the experience of the illusion, if possible.")
                )
            ],
            button_label=_('Start')
        )
        # read consent form from file
        rendered = render_to_string(
            'consent_speech2song.html')

        consent = Consent.action(
            rendered, title=_('Informed consent'), confirm=_('I agree'), deny=_('Stop'))

        playlist = Playlist.action(experiment.playlists.all())

        start_session = StartSession.action()

        return combine_actions(
            explainer,
            consent,
            playlist,
            start_session
        )

    @staticmethod
    def next_round(session):
        next_round = session.get_next_round()
        blocks = [1, 2, 3]
        # shuffle blocks based on session.id as seed -> always same order for same session
        np.random.seed(session.id)
        np.random.shuffle(blocks)
        # group_ids for practice (0), or one of the speech blocks (1-3)
        actions = []
        is_speech = True
        if next_round == 1:
            explainer = Explainer.action(
                instruction=_(
                    'Thank you for answering these questions about your background!'),
                steps=[
                    Explainer.step(
                        description=_(
                            'Now you will hear a sound repeated multiple times.')
                    ),
                    Explainer.step(
                        description=_(
                            'Please listen to the following segment carefully, if possible with headphones.')
                    ),
                ],
                button_label=_('OK')
            )
            return combine_actions(
                *get_participant_info(),
                *get_language_info(),
                explainer,
                # *next_repeated_representation(session, is_speech, 0)
            )
        elif next_round == 2:
            e1 = Explainer.action(
                instruction=_('Previous studies have shown that many people perceive the segment you just heard as song-like after repetition, but it is no problem if you do not share that perception because there is a wide range of individual differences.'),
                steps=[],
                button_label=_('Continue')
            )
            e2 = Explainer.action(
                instruction=_('Part 1'),
                steps=[
                    Explainer.step(
                        description=_('In the first part of the experiment, you will be presented with speech segments like the one just now in different languages which you may or may not speak.')),
                    Explainer.step(
                        description=_('Your task is to rate each segment on a scale from 1 to 5.'))
                ],
                button_label=_('Continue')
            )
            actions.extend([e1, e2])
            group_id = blocks[0]
        elif 2 < next_round <= n_rounds_per_block + 1:
            group_id = blocks[0]
        elif n_rounds_per_block + 1 < next_round <= 2 * n_rounds_per_block + 1:
            group_id = blocks[1]
        elif 2 * n_rounds_per_block + 1 < next_round <= 3 * n_rounds_per_block + 1:
            group_id = blocks[2]
        elif next_round == 3 * n_rounds_per_block + 2:
            # Final block (environmental sounds)
            e3 = Explainer.action(
                instruction=_('Part2'),
                steps=[
                    Explainer.step(
                        description=_(
                            'In the following part of the experiment, you will be presented with segments of environmental sounds as opposed to speech sounds.')
                    ),
                    Explainer.step(
                        description=_('Environmental sounds are sounds that are not speech nor music.')
                    ),
                    Explainer.step(
                        description=_('Like the speech segments, your task is to rate each segment on a scale from 1 to 5.')
                    )
                ],
                button_label=_('Continue')
            )
            actions.append(e3)
            group_id = 4
            is_speech = False
        elif 3 * n_rounds_per_block + 2 < next_round <= 4 * n_rounds_per_block + 1:
            group_id = 4
            is_speech = False
        else:
            # Finish session
            session.finish()
            session.save()

            # Return a score and final score action
            return Final.action(
                title=_('End of experiment'),
                session=session,
                score_message=_(
                    'Thank you for contributing your time to science!')
            )

        if next_round % 2 == 0:
            # even round: single representation (first round are questions only)
            actions.extend(next_single_representation(
                session, is_speech, group_id))
        else:
            # uneven round: repeated representation
            actions.extend(next_repeated_representation(
                session, is_speech))
        return combine_actions(*actions)


def next_single_representation(session, is_speech, group_id):
    """ combine a question after the first representation,
    and several repeated representations of the sound,
    with a final question"""
    filter_by = {'group_id': group_id}
    section = session.section_from_unused_song(filter_by)
    actions = [sound(section), speech_or_sound_question(is_speech)]
    return actions


def next_repeated_representation(session, is_speech, group_id=-1):
    if group_id >= 0:
        # for the Test case, there is no previous section to look at
        section = session.playlist.section_set.get(group_id=group_id)
    else:
        section = session.previous_section()
    actions = [sound(section, i) for i in range(1, n_representations+1)]
    actions.append(speech_or_sound_question(is_speech))
    return actions


def speech_or_sound_question(is_speech):
    if is_speech:
        return question_speech()
    else:
        return question_sound()


def question_speech():
    return Question.radios(
        key='speech2song',
        question=_('Does this sound like song or speech to you?'),
        choices=[
            _('sounds exactly like speech'),
            _('sounds somewhat like speech'),
            _('sounds neither like speech nor like song'),
            _('sounds somewhat like song'),
            _('sounds exactly like song')],
        view=Question.ID_RESULT_QUESTION
    )


def question_sound():
    return Question.radios(
        key='sound2music',
        question=_(
            'Does this sound like music or an environmental sound to you?'),
        choices=[
            _('sounds exactly like an environmental sound'),
            _('sounds somewhat like an environmental sound'),
            _('sounds neither like an environmental sound nor like music'),
            _('sounds somewhat like music'),
            _('sounds exactly like music')],
        view=Question.ID_RESULT_QUESTION
    )


def get_participant_info():
    return [
        question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_gender_identity'),
        question_by_key('dgf_country_of_origin_open', EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_country_of_residence_open', EXTRA_DEMOGRAPHICS),
    ]


def get_language_info():
    return [
        question_by_key('lang_mother', LANGUAGE),
        question_by_key('lang_second', LANGUAGE),
        question_by_key('lang_third', LANGUAGE),
        LanguageQuestion(_('English')).exposure_question(),
        LanguageQuestion(_('Brazilian Portuguese')).exposure_question(),
        LanguageQuestion(_('Mandarin Chinese')).exposure_question()
    ]


def sound(section, n_representation=None):
    title = _('Listen carefully')
    instructions = {
        'preload': '',
        'during_representation': ''
    }
    view = CompositeView(
            section=section,
            feedback_form=None,
            instructions=instructions,
            title=title
    )
    if n_representation and n_representation > 1:
        ready_time = 0
    else:
        ready_time = 1
    config = {
        'ready_time': ready_time,
        'decision_time': section.duration + .5,
        'show_animation': False
    }
    return view.action(config=config)
