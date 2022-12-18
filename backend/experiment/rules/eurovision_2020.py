import random
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from .views import SongSync,  Final, Score, Explainer, Consent, StartSession, Playlist, Step, Trial
from .views.playback import Playback
from .views.form import BooleanQuestion, Form
from .util.questions import DEMOGRAPHICS, next_question
from .util.goldsmiths import MSI_FG_GENERAL, MSI_ALL
from .util.stomp import STOMP20
from .util.tipi import TIPI
from .util.actions import combine_actions


class Eurovision2020(Base):
    """Rules for the Eurovision 2020 version of the Hooked experiment.

    Based on the MBCS internship projects of Ada Orken and and Leanne Kuiper.
    """

    ID = 'EUROVISION_2020'
    timeout = 15

    @classmethod
    def first_round(cls, experiment, participant):
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
        rendered = render_to_string(
            'consent/consent_eurovision_2020.html')
        consent = Consent.action(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))

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
    def plan_sections(cls, session):
        """Set the plan of tracks for a session.

        N.B. Assumes exactly one segment each of tags 1, 2, and 3 per song!
        """

        # Which songs are available?
        free_song_set = set(session.playlist.song_ids({'tag__lt': 3}))
        old_new_song_set = set(session.playlist.song_ids({'tag__gt': 0}))

        # How many sections do we need?
        n_old = round(0.17 * session.experiment.rounds)
        n_new = round(0.33 * session.experiment.rounds) - n_old
        n_free = session.experiment.rounds - 2 * n_old - n_new

        # Assign songs.
        old_songs = random.sample(old_new_song_set, k=n_old)
        free_songs = random.sample(free_song_set - set(old_songs), k=n_free)
        new_songs = \
            random.sample(
                old_new_song_set - set(old_songs + free_songs),
                k=n_new
            )

        # Assign tags for Block 2. Technically 1 and 2 are also OK for the
        # 'free' sections in Block 1, but it is easier just to set tag 0.
        free_tags = [0] * n_free
        old_tags_1 = random.choices([1, 2], k=n_old)
        condition = random.choice(['same', 'different', 'karaoke'])
        if condition == 'karaoke':
            old_tags_2 = [3] * n_old
            new_tags = [3] * n_new
        # Reverse tags 1 and 2 for the 'different' condition.
        elif condition == 'different':
            old_tags_2 = [3 - tag for tag in old_tags_1]
            new_tags = random.choices([1, 2], k=n_new)
        else:  # condition == 'same'
            old_tags_2 = old_tags_1
            new_tags = random.choices([1, 2], k=n_new)

        # Randomise.
        permutation_1 = random.sample(range(n_free + n_old), n_free + n_old)
        permutation_2 = random.sample(range(n_old + n_new), n_old + n_new)
        plan = {
            'n_song_sync': n_free + n_old,
            'n_heard_before': n_old + n_new,
            'condition': condition,
            'songs': (
                [(free_songs + old_songs)[i] for i in permutation_1]
                + [(old_songs + new_songs)[i] for i in permutation_2]
            ),
            'tags': (
                [(free_tags + old_tags_1)[i] for i in permutation_1]
                + [(old_tags_2 + new_tags)[i] for i in permutation_2]
            ),
            'novelty': (
                [(['free'] * n_free + ['old'] * n_old)[i]
                 for i in permutation_1]
                + [(['old'] * n_old + ['new'] * n_new)[i]
                   for i in permutation_2]
            )
        }

        # Save, overwriting existing plan if one exists.
        session.merge_json_data({'plan': plan})
        # session.save() is required for persistence
        session.save()

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
            next_question(
                session,
                random.sample(DEMOGRAPHICS, len(DEMOGRAPHICS)),
            )

        # 2. General music sophistication (18 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(MSI_FG_GENERAL, len(MSI_FG_GENERAL)),
                )

        # 3. Complete music sophistication (20 questions)
        if question is None:
            # next_question() will skip the FG questions from before
            question = \
                next_question(
                    session,
                    random.sample(MSI_ALL, len(MSI_ALL)),
                )

        # 4. STOMP (20 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(STOMP20, len(STOMP20)),
                )

        # 5. TIPI (10 questions)
        if question is None:
            question = \
                next_question(
                    session,
                    random.sample(TIPI, len(TIPI)),
                )

        return Trial(
                title=_("Questionnaire"),
                feedback_form=Form([question], is_profile=True, is_skippable=question.is_skippable)).action()


    @staticmethod
    def next_round(session):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if session.rounds_complete():

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            return combine_actions(
                Score(session).action(),
                Final(
                    session=session,
                    final_text=Eurovision2020.final_score_message(session),
                    rank=Eurovision2020.rank(session),
                    show_social=True,
                    show_profile_link=True,
                    button={'text': _('Play again'), 'link': '{}/{}'.format(settings.CORS_ORIGIN_WHITELIST[0], session.experiment.slug)}
                ).action()
            )

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_next_round()

        # Collect actions.
        actions = []

        if next_round_number == 1:
            # Plan sections
            Eurovision2020.plan_sections(session)

            # Go to SongSync straight away.
            actions.append(Eurovision2020.next_song_sync_action(session))
        else:
            # Create a score action.
            actions.append(Score(session).action())

            # Load the heard_before offset.
            try:
                heard_before_offset = \
                    session.load_json_data()['plan']['n_song_sync'] + 1
            except KeyError as error:
                print('Missing plan key: %s' % str(error))
                return combine_actions(*actions)

            # SongSync rounds. Skip questions until Round 5.
            if next_round_number in range(2, 5):
                actions.append(Eurovision2020.next_song_sync_action(session))
            if next_round_number in range(5, heard_before_offset):
                actions.append(Eurovision2020.get_random_question(session))
                actions.append(Eurovision2020.next_song_sync_action(session))

            # HeardBefore rounds
            if next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(Eurovision2020.heard_before_explainer())
                actions.append(
                    Eurovision2020.next_heard_before_action(session))
            if next_round_number > heard_before_offset:
                actions.append(Eurovision2020.get_random_question(session))
                actions.append(
                    Eurovision2020.next_heard_before_action(session))

        return combine_actions(*actions)

    @classmethod
    def next_song_sync_action(cls, session):
        """Get next song_sync section for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            songs = plan['songs']
            tags = plan['tags']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(songs) and next_round_number <= len(tags):
            section = \
                session.section_from_song(
                    songs[next_round_number - 1],
                    {'tag': tags[next_round_number - 1]}
                )
        if not section:
            print("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        result_id = cls.prepare_result(session, section)
        return SongSync(
            section=section,
            title=cls.get_trial_title(session, next_round_number),
            result_id=result_id,
            scoring_rule='SONG_SYNC'
        ).action()

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

    @classmethod
    def next_heard_before_action(cls, session):
        """Get next heard_before action for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            songs = plan['songs']
            tags = plan['tags']
            novelty = plan['novelty']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(songs) and next_round_number <= len(tags):
            section = \
                session.section_from_song(
                    songs[next_round_number - 1],
                    {'tag': tags[next_round_number - 1]}
                )
        if not section:
            print("Warning: no heard_before section found")
            section = session.section_from_any_song()

        playback = Playback(
            [section],
            play_config={'ready_time': 3, 'show_animation': True},
            preload_message=_('Get ready!'))
        expected_result=int(novelty[next_round_number - 1] == 'old')
        # create Result object and save expected result to database
        result_pk = cls.prepare_result(session, section, expected_result)
        form = Form([BooleanQuestion(
            key='heard_before',
            choices={
                'new': _("NO"),
                'old': _("YES"),
            },
            question=_("Did you hear this song in previous rounds?"),
            result_id=result_pk,
            scoring_rule='REACTION_TIME',
            submits=True)])
        config = {
            'style': 'boolean-negative-first',
            'auto_advance': True,
            'decision_time': cls.timeout
        }
        trial = Trial(
            title=cls.get_trial_title(session, next_round_number),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial.action()

    @classmethod
    def get_trial_title(cls, session, next_round_number):
        return _('Round {} / {}').format(next_round_number, session.experiment.rounds)

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
                    if json_data['config']['expected_result'] == 1:
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
