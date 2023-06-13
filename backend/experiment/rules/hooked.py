import random
import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from experiment.actions import  Consent, Explainer, Final, Playlist, Score, SongSync, StartSession, Step, Trial
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.playback import Playback
from experiment.questions.demographics import DEMOGRAPHICS
from experiment.questions.utils import unasked_question
from experiment.questions.goldsmiths import MSI_FG_GENERAL, MSI_ALL
from experiment.questions.stomp import STOMP20
from experiment.questions.tipi import TIPI
from experiment.actions.styles import STYLE_BOOLEAN_NEGATIVE_FIRST
from result.utils import prepare_result

logger = logging.getLogger(__name__)


class Hooked(Base):
    """Superclass for Hooked experiment rules"""

    consent_file = 'consent_hooked.html';
    timeout = 15
    questions = True
    round_modifier = 0

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""
        
        # 1. Explain game.
        explainer = Explainer(
            instruction="How to Play",
            steps=[
                Step(_(
                    "Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn.")),
                Step(_(
                    "Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!")),
                Step(_(
                    "Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"))
            ],
            button_label=_("Let's go!")).action(True)

        # 2. Get informed consent.
        if  cls.consent_file:
            rendered = render_to_string('consent/{}'.format(cls.consent_file))
            consent = Consent.action(text=rendered, title=_('Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        else:
            # fall back to lorem ipsum if no consent_file is defined
            consent = Consent.action()

        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            consent,
            playlist,
            start_session
        ]


    @classmethod
    def get_random_question(cls, session):
        """Get a random question from each question list, in priority completion order.

        Participants will not continue to the next question set until they
        have completed their current one.
        """

        # Constantly re-randomising is mildly inefficient, but it's not
        # worth the trouble to save blocked, randomised question lists persistently.

        # 1. Demographic questions (7 questions)
        question = \
            unasked_question(
                session.participant,
                DEMOGRAPHICS,
                randomize=True
            )

        # 2. General music sophistication (18 questions)
        if question is None:
            question = \
                unasked_question(
                    session.participant,
                    MSI_FG_GENERAL,
                    randomize=True
                )

        # 3. Complete music sophistication (20 questions)
        if question is None:
            # next_question() will skip the FG questions from before
            question = \
                unasked_question(
                    session.participant,
                    MSI_ALL,
                    randomize=True
                )

        # 4. STOMP (20 questions)
        if question is None:
            question = \
                unasked_question(
                    session.participant,
                    STOMP20,
                    randomize=True
                )

        # 5. TIPI (10 questions)
        if question is None:
            question = \
                unasked_question(
                    session.participant,
                    TIPI,
                    randomize=True
                )
        
        if question is None:
            return None

        return Trial(
                title=_("Questionnaire"),
                feedback_form=Form([question], is_skippable=question.is_skippable)).action()


    
    @classmethod
    def next_round(cls, session):
        """Get action data for the next round"""
        json_data = session.load_json_data()

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if session.rounds_complete():

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            next_round_number = session.get_next_round()
            config = {'show_section': True, 'show_total_score': True}
            title = cls.get_trial_title(session, next_round_number - 1)
            return [
                Score(session,
                    config=config,
                    title=title
                ).action(),
                Final(
                    session=session,
                    final_text=cls.final_score_message(session),
                    rank=cls.rank(session),
                    show_social=True,
                    show_profile_link=True,
                    button={'text': _('Play again'), 'link': '{}/{}'.format(settings.CORS_ORIGIN_WHITELIST[0], session.experiment.slug)}
                ).action()
            ]

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_next_round()

        # Collect actions.
        actions = []

        if next_round_number == 1:
            # Plan sections
            cls.plan_sections(session)

            # Go to SongSync straight away.
            actions.append(cls.next_song_sync_action(session))
        else:
            # Create a score action.
            config = {'show_section': True, 'show_total_score': True}
            title = cls.get_trial_title(session, next_round_number - 1)
            actions.append(Score(session,
                config=config,
                title=title
            ).action())

            # Load the heard_before offset.
            plan = json_data.get('plan')
            heard_before_offset = plan['n_song_sync'] + 1

            # SongSync rounds. Skip questions until Round 5.
            if next_round_number in range(2, 5):
                actions.append(cls.next_song_sync_action(session))
            if next_round_number in range(5, heard_before_offset):
                actions.append(cls.get_random_question(session)) if cls.questions else None
                actions.append(cls.next_song_sync_action(session))

            # HeardBefore rounds
            if next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(cls.heard_before_explainer())
                actions.append(
                    cls.next_heard_before_action(session))
            if next_round_number > heard_before_offset:
                actions.append(cls.get_random_question(session)) if cls.questions else None
                actions.append(
                    cls.next_heard_before_action(session))

        return actions


    @staticmethod
    def heard_before_explainer():
        """Explainer for heard-before rounds"""
        return Explainer(
            instruction=_("Bonus Rounds"),
            steps=[
                Step(_("Listen carefully to the music.")),
                Step(_("Did you hear the same song during previous rounds?")),
            ],
            button_label=_("Continue")).action(True)

    @staticmethod
    def final_score_message(session):
        """Create final score message for given session"""

        n_sync_guessed = 0
        sync_time = 0
        n_sync_correct = 0
        n_old_new_expected = 0
        n_old_new_correct = 0

        for result in session.result_set.all():
            json_data = result.load_json_data()
            try:
                if json_data['view'] == 'SONG_SYNC':
                    if json_data['result']['type'] == 'recognized':
                        n_sync_guessed += 1
                        sync_time += json_data['result']['recognition_time']
                        if result.score > 0:
                            n_sync_correct += 1
                else:
                    if result.expected_response == 'old':
                        n_old_new_expected += 1
                        if result.score > 0:
                            n_old_new_correct += 1
            except KeyError as error:
                print('KeyError: %s' % str(error))
                continue

        score_message = "Well done!" if session.final_score > 0 else "Too bad!"
        if n_sync_guessed == 0:
            song_sync_message = "You did not recognise any songs at first."
        else:
            song_sync_message = "It took you {} s to recognise a song on average, and you correctly identified {} out of the {} songs you thought you knew.".format(
                round(sync_time / n_sync_guessed, 1), n_sync_correct, n_sync_guessed)
        heard_before_message = "During the bonus rounds, you remembered {} of the {} songs that came back.".format(
            n_old_new_correct, n_old_new_expected)
        return score_message + " " + song_sync_message + " " + heard_before_message

    @classmethod
    def get_trial_title(cls, session, next_round_number):    
        return _("Round %(number)d / %(total)d") %\
            {'number': next_round_number, 'total': session.experiment.rounds}
    
    @classmethod
    def plan_sections(cls, session, filter_by={}):
        """Set the plan of tracks for a session.
        """

        # Which songs are available?
        songs = list(session.playlist.song_ids(filter_by))
        random.shuffle(songs)

        # How many sections do we need?
        # 2/3 of the rounds are SongSync, of which 1/4 old songs, 3/4 "free"
        # 1/3 of the rounds are "heard before", of which 1/2 old songs
        # e.g. 30 rounds -> 20 SongSync with 5 songs to be repeated later
        n_rounds = session.experiment.rounds
        n_old = round(0.17 * n_rounds)
        n_new = round(0.17 * n_rounds)
        n_free = n_rounds - 2 * n_old - n_new

        # Assign songs.
        old_songs = songs[:n_old]
        new_songs = songs[n_old:n_old+n_new]
        free_songs = songs[n_old+n_new:n_old+n_new+n_free]

        # Assign sections.
        old_sections = [session.section_from_song(s) for s in old_songs]
        free_sections = [session.section_from_song(s) for s in free_songs]
        new_sections = [session.section_from_song(s) for s in new_songs]

        # Randomise.
        old_section_info = [{'novelty': 'old', 'id': s.id}
                            for s in old_sections]
        song_sync_sections = old_section_info + [
            {'novelty': 'free', 'id': s.id} for s in free_sections]
        random.shuffle(song_sync_sections)
        heard_before_sections = old_section_info + [
            {'novelty': 'new', 'id': s.id} for s in new_sections]
        random.shuffle(heard_before_sections)
        plan = {
            'song_sync_sections': song_sync_sections,
            'n_song_sync': len(song_sync_sections),
            'heard_before_sections': heard_before_sections
        }

        # Save, overwriting existing plan if one exists.
        session.save_json_data({'plan': plan})

    @classmethod
    def next_song_sync_action(cls, session):
        """Get next song_sync section for this session."""

        # Load plan.
        next_round_number = session.get_current_round() - cls.round_modifier
        try:
            plan = session.load_json_data()['plan']
            sections = plan['song_sync_sections']
        except KeyError as error:
            logger.error('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(sections):
            section = \
                session.section_from_any_song(
                    {'id': sections[next_round_number-1].get('id')})
        if not section:
            logger.warning("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        key = 'song_sync'
        result_id = prepare_result(key, session, section=section, scoring_rule='SONG_SYNC')
        return SongSync(
            section=section,
            title=cls.get_trial_title(session, next_round_number),
            key=key,
            result_id=result_id
        ).action()
    
    @classmethod
    def next_heard_before_action(cls, session):
        """Get next heard_before action for this session."""

        # Load plan.
        next_round_number = session.get_current_round() - cls.round_modifier
        try:
            plan = session.load_json_data()['plan']
            sections = plan['heard_before_sections']
            heard_before_offset = len(plan['song_sync_sections']) + 1
        except KeyError as error:
            logger.error('Missing plan key: %s' % str(error))
            return None
        # Get section.
        section = None
        if next_round_number - heard_before_offset  <= len(sections):
            this_section_info = sections[next_round_number - heard_before_offset]
            section = session.section_from_any_song(
                    {'id': this_section_info.get('id')})
        if not section:
            logger.warning("Warning: no heard_before section found")
            section = session.section_from_any_song()
        playback = Playback(
            [section],
            play_config={'ready_time': 3, 'show_animation': True},
            preload_message=_('Get ready!'))
        expected_response = this_section_info.get('novelty')
        # create Result object and save expected result to database
        key = 'heard_before'
        form = Form([BooleanQuestion(
            key=key,
            choices={
                'new': _("NO"),
                'old': _("YES"),
            },
            question=_("Did you hear this song in previous rounds?"),
            result_id=prepare_result(key, session, section=section, expected_response=expected_response, scoring_rule='REACTION_TIME',),
            submits=True,
            style={STYLE_BOOLEAN_NEGATIVE_FIRST: True, 'buttons-large-gap': True})
            ])
        config = {
            'auto_advance': True,
            'response_time': cls.timeout
        }
        trial = Trial(
            title=cls.get_trial_title(session, next_round_number),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial.action()
