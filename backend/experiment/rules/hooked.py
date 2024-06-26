import logging
import random

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, Score, Step, Trial
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.styles import STYLE_BOOLEAN_NEGATIVE_FIRST
from experiment.actions.wrappers import song_sync
from question.questions import QUESTION_GROUPS
from result.utils import prepare_result


logger = logging.getLogger(__name__)


class Hooked(Base):
    """Superclass for Hooked experiment rules"""
    ID = 'HOOKED'

    consent_file = 'consent/consent_hooked.html'
    recognition_time = 15  # response time for "Do you know this song?"
    sync_time = 15  # response time for "Did the track come back in the right place?"
    # if the track continues in the wrong place: minimal shift forward (in seconds)
    min_jitter = 10
    # if the track continutes in the wrong place: maximal shift forward (in seconds)
    max_jitter = 15
    heard_before_time = 15  # response time for "Have you heard this song in previous rounds?"
    questions = True
    relevant_keys = ['recognize', 'heard_before']
    round_modifier = 0
    play_method = 'BUFFER'

    def __init__(self):
        self.question_series = [
            {"name": "DEMOGRAPHICS", "keys": QUESTION_GROUPS["DEMOGRAPHICS"], "randomize": True}, # 1. Demographic questions (7 questions)
            {"name": "MSI_OTHER", "keys": ['msi_39_best_instrument'], "randomize": False},
            {"name": "MSI_FG_GENERAL", "keys": QUESTION_GROUPS["MSI_FG_GENERAL"], "randomize": True}, # 2. General music sophistication
            {"name": "MSI_ALL", "keys": QUESTION_GROUPS["MSI_ALL"], "randomize": True}, # 3. Complete music sophistication (20 questions)
            {"name": "STOMP20", "keys": QUESTION_GROUPS["STOMP20"], "randomize": True}, # 4. STOMP (20 questions)
            {"name": "TIPI", "keys": QUESTION_GROUPS["TIPI"], "randomize": True}, # 5. TIPI (10 questions)
        ]

    def first_round(self, experiment):
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
            step_numbers=True,
            button_label=_("Let's go!"))

        # 2. Add consent from file or admin (admin has priority)
        consent = Consent(
            experiment.consent,
            title=_('Informed consent'),
            confirm=_('I agree'),
            deny=_('Stop'),
            url=self.consent_file
            )
        
        # 3. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        return [
            consent,
            playlist,
            explainer,
        ]

    def next_round(self, session):
        """Get action data for the next round"""
        json_data = session.load_json_data()
        round_number = self.get_current_round(session)

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if round_number == session.experiment.rounds:

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            total_score = session.total_score()
            return [
                self.get_score(session, round_number),
                Final(
                    session=session,
                    final_text=self.final_score_message(session),
                    rank=self.rank(session),
                    social=self.social_media_info(
                        session.experiment, total_score),
                    show_profile_link=True,
                    button={
                        'text': _('Play again'),
                        'link': self.get_play_again_url(session),
                    }
                )
            ]

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.

        # Collect actions.
        actions = []

        if round_number == 0:
            # Plan sections
            self.plan_sections(session)
            # Go to SongSync straight away.
            actions.extend(self.next_song_sync_action(session))
        else:
            # Create a score action.
            actions.append(self.get_score(session, round_number))

            # Load the heard_before offset.
            plan = json_data.get('plan')
            heard_before_offset = plan['n_song_sync']

            # SongSync rounds. Skip questions until Round 5.
            if round_number in range(1, 5):
                actions.extend(self.next_song_sync_action(session))
            if round_number in range(5, heard_before_offset):
                question_trial = self.get_single_question(session)
                if question_trial:
                    actions.append(question_trial)
                actions.extend(self.next_song_sync_action(session))

            # HeardBefore rounds
            if round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(
                    self.next_heard_before_action(session))
            if round_number > heard_before_offset:
                question_trial = self.get_single_question(session)
                if question_trial:
                    actions.append(question_trial)
                actions.append(
                    self.next_heard_before_action(session))

        return actions

    def get_current_round(self, session):
        return session.get_relevant_results(self.relevant_keys).count()

    def heard_before_explainer(self):
        """Explainer for heard-before rounds"""
        return Explainer(
            instruction=_("Bonus Rounds"),
            steps=[
                Step(_("Listen carefully to the music.")),
                Step(_("Did you hear the same song during previous rounds?")),
            ],
            step_numbers=True,
            button_label=_("Continue"))

    def final_score_message(self, session):
        """Create final score message for given session"""

        n_sync_guessed = 0
        sync_time = 0
        n_sync_correct = 0
        n_old_new_expected = 0
        n_old_new_correct = 0

        for result in session.result_set.all():
            if result.question_key == 'recognize':
                if result.given_response == 'yes':
                    n_sync_guessed += 1
                    json_data = result.load_json_data()
                    sync_time += json_data.get('decision_time')
                    if result.score > 0:
                        n_sync_correct += 1
            else:
                if result.expected_response == 'old':
                    n_old_new_expected += 1
                    if result.score > 0:
                        n_old_new_correct += 1

        score_message = "Well done!" if session.final_score > 0 else "Too bad!"
        if n_sync_guessed == 0:
            song_sync_message = "You did not recognise any songs at first."
        else:
            song_sync_message = "It took you {} s to recognise a song on average, and you correctly identified {} out of the {} songs you thought you knew.".format(
                round(sync_time / n_sync_guessed, 1), n_sync_correct, n_sync_guessed)
        heard_before_message = "During the bonus rounds, you remembered {} of the {} songs that came back.".format(
            n_old_new_correct, n_old_new_expected)
        return score_message + " " + song_sync_message + " " + heard_before_message

    def get_trial_title(self, session, round_number):
        return _("Round %(number)d / %(total)d") %\
            {'number': round_number+1, 'total': session.experiment.rounds}

    def plan_sections(self, session, filter_by={}):
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
        old_songs = songs[:n_old]  # will reappear in "heard before" rounds
        # novel songs in "heard before" rounds
        new_songs = songs[n_old:n_old+n_new]
        # will not reappear in "heard before" rounds
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

    def next_song_sync_action(self, session, explainers=[]):
        """Get next song_sync section for this session."""

        # Load plan.
        round_number = self.get_current_round(session) - self.round_modifier
        try:
            plan = session.load_json_data()['plan']
            sections = plan['song_sync_sections']
        except KeyError as error:
            logger.error('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if round_number <= len(sections):
            section = \
                session.playlist.section_set.get(
                    **{'id': sections[round_number-1].get('id')})
        if not section:
            logger.warning("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        return song_sync(session, section, title=self.get_trial_title(session, round_number),
                         recognition_time=self.recognition_time, sync_time=self.sync_time,
                         min_jitter=self.min_jitter, max_jitter=self.max_jitter)

    def next_heard_before_action(self, session):
        """Get next heard_before action for this session."""
        round_number = self.get_current_round(session) - self.round_modifier
        # Load plan.
        try:
            plan = session.load_json_data()['plan']
            sections = plan['heard_before_sections']
            heard_before_offset = len(plan['song_sync_sections']) + 1
        except KeyError as error:
            logger.error('Missing plan key: %s' % str(error))
            return None
        # Get section.
        section = None
        if round_number - heard_before_offset <= len(sections):
            this_section_info = sections[round_number - heard_before_offset]
            section = session.playlist.section_set.get(
                **{'id': this_section_info.get('id')})
        if not section:
            logger.warning("Warning: no heard_before section found")
            section = session.section_from_any_song()
        playback = Autoplay(
            [section],
            show_animation=True,
            preload_message=_('Get ready!')
        )
        expected_response = this_section_info.get('novelty')
        # create Result object and save expected result to database
        key = 'heard_before'
        form = Form([BooleanQuestion(
            key=key,
            choices={
                'new': _("No"),
                'old': _("Yes"),
            },
            question=_("Did you hear this song in previous rounds?"),
            result_id=prepare_result(
                key, session, section=section, expected_response=expected_response, scoring_rule='REACTION_TIME',),
            submits=True,
            style={STYLE_BOOLEAN_NEGATIVE_FIRST: True, 'buttons-large-gap': True})
        ])
        config = {
            'auto_advance': True,
            'response_time': self.heard_before_time
        }
        trial = Trial(
            title=self.get_trial_title(session, round_number),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial

    def get_score(self, session, round_number):
        config = {'show_section': True, 'show_total_score': True}
        title = self.get_trial_title(session, round_number - 1)
        previous_score = session.get_previous_result(self.relevant_keys).score
        return Score(session,
                     config=config,
                     title=title,
                     score=previous_score
                     )
