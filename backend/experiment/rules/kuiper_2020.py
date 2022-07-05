import random

from django.utils.translation import gettext_lazy as _

from .base import Base
from .views import SongSync, SongBool, FinalScore, Score, Explainer, Consent, Playlist, StartSession, Step, Trial
from .views.form import BooleanQuestion, Form
from .util.questions import DEMOGRAPHICS, next_question
from .util.goldsmiths import MSI_FG_GENERAL, MSI_ALL
from .util.stomp import STOMP20
from .util.tipi import TIPI
from .util.actions import combine_actions


class Kuiper2020(Base):
    """Rules for the Christmas version of the Hooked experiment.

    Based on the MBCS internship projects of Leanne Kuiper.
    """

    ID = 'KUIPER_2020'

    @staticmethod
    def first_round(experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer.action(
            instruction="How to Play",
            steps=[
                Step(_("Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn.",)),
                Step(_("Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!")),
                Step(_("Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"))
            ],
            step_numbers=True
        )

        # 2. Get informed consent.
        consent = Consent.action(
            """
<p>You will be taking part in the Hooked on Music research project conducted by Dr John Ashley Burgoyne of the Music Cognition Group at the University of Amsterdam’s Institute for Logic, Language, and Computation. Before the research project can begin, it is important that you read about the procedures we will be applying. Make sure to read this information carefully.</p>

<h4>Purpose of the Research Project</h4>

<p>What makes music catchy? Why do some pieces of music come back to mind after we hear just a few notes and others not? Is there one ‘recipe’ for memorable music or does it depend on the person? And are there differences between what makes it easy to remember music for the long term and what makes it easy to remember music right now?</p>

<p>This project will help us answer these questions and better understand how we remember music both over the short term and the long term. Musical memories are fundamentally associated with developing our identities in adolescence, and even as other memories fade in old age, musical memories remain intact. Understanding musical memory better can help composers write new music, search engines find and recommend music their users will enjoy, and music therapists develop new approaches for working and living with memory disorders.</p>

<h4>Who Can Take Part in This Research?</h4>

<p>Anybody with sufficiently good hearing, natural or corrected, to enjoy music listening is welcome to participate in this research. Your device must be able to play audio, and you must have a sufficiently strong data connection to be able to stream short MP3 files. Headphones are recommended for the best results, but you may also use either internal or external loudspeakers. You should adjust the volume of your device so that it is comfortable for you.</p>

<h4>Instructions and Procedure</h4>

<p>You will be presented with short fragments of music and asked whether you recognise them. Try to answer as quickly as you can, but only at the moment that you find yourself able to ‘sing along’ in your head. When you tell us that you recognise a piece of music, the music will keep playing, but the sound will be muted for a few seconds. Keep following along with the music in your head, until the music comes back. Sometimes it will come back in the right place, but at other times, we will have skipped forward or backward within the same piece of music during the silence. We will ask you whether you think the music came back in the right place or not. In between fragments, we will ask you some simple survey questions to better understand your musical background and how you engage with music in your daily life.</p>

<p>In a second phase of the experiment, you will also be presented with short fragments of music, but instead of being asked whether you recognise them, you will be asked whether you heard them before while participating in the first phase of the experiment. Again, in between these fragments, we will ask you simple survey questions about your musical background and how you engage with music in your daily life.</p>

<h4>Voluntary Participation</h4>

<p>You will be participating in this research project on a voluntary basis. This means you are free to stop taking part at any stage. This will not have any personal consequences and you will not be obliged to finish the procedures described above. You can also decide to withdraw your participation up to 8 days after the research has ended. If you decide to stop or withdraw your consent, all the information gathered up until then will be permanently deleted.</p>

<h4>Discomfort, Risks, and Insurance</h4>

<p>The risks of participating in this research are no greater than in everyday situations at home. Previous experience in similar research has shown that no or hardly any discomfort is to be expected for participants. For all research at the University of Amsterdam, a standard liability insurance applies.</p>

<h4>Confidential Treatment of Your Details</h4>

<p>The information gathered over the course of this research will be used for further analysis and publication in scientific journals only. Fully anonymised data collected during the experiment (e.g., whether each musical fragment was recognised and how long it took) may be made available online in tandem with these scientific publications. Your personal details will not be used in these publications, and we guarantee that you will remain anonymous under all circumstances.</p>

<h4>Further Information</h4>

<p>For further information on the research project, please contact John Ashley Burgoyne (phone number: +31 20 525 7034; e-mail: j.a.burgoyne@uva.nl; Science Park 107, 1098 GE Amsterdam).</p>

<p>If you have any complaints regarding this research project, you can contact the secretary of the Ethics Committee of the Faculty of Humanities of the University of Amsterdam (phone number: +31 20 525 3054; e-mail: commissie-ethiek-fgw@uva.nl; Kloveniersburgwal 48, 1012 CX Amsterdam).</p>

<h4>Informed Consent</h4>

<p>I hereby declare that I have been clearly informed about the research project Hooked on Music at the University of Amsterdam, Institute for Logic, Language and Computation, conducted by John Ashley Burgoyne as described above.</p>

<p>I consent to participate in this research on an entirely voluntary basis. I retain the right to revoke this consent without having to provide any reasons for my decision. I am aware that I am entitled to discontinue the research at any time and can withdraw my participation up to 8 days after the research has ended. If I decide to stop or withdraw my consent, all the information gathered up until then will be permanently deleted.</p>

<p>If my research results are used in scientific publications or made public in any other way, they will be fully anonymised. My personal information may not be viewed by third parties without my express permission.</p>
            """
        )

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

    @staticmethod
    def plan_sections(session):
        """Set the plan of tracks for a session.

           Assumes that all tags of 1 have a corresponding tag of 2
           with the same group_id, and vice-versa.
        """

        # Which songs are available?
        free_song_set = set(session.playlist.song_ids())
        old_new_song_set = set(session.playlist.song_ids({'tag_id__gt': 0}))

        # How many sections do we need?
        n_old = round(0.17 * session.experiment.rounds)
        n_new = round(0.33 * session.experiment.rounds) - n_old
        n_free = session.experiment.rounds - 2 * n_old - n_new

        # Assign songs.
        old_songs = random.sample(old_new_song_set, k=n_old)
        free_songs = random.sample(free_song_set - set(old_songs), k=n_free)
        new_songs = \
            random.sample(free_song_set - set(old_songs + free_songs), k=n_new)

        # Assign sections.
        condition = random.choice(['same', 'different'])
        old_sections_1 = [session.section_from_song(s) for s in old_songs]
        if condition == 'same':
            old_sections_2 = old_sections_1
        else:
            old_sections_2 = \
                [session.
                 section_from_any_song(
                     {'group_id': s.group_id, 'tag_id': 3 - s.tag_id}
                 )
                 for s in old_sections_1]
        free_sections = [session.section_from_song(s) for s in free_songs]
        new_sections = [session.section_from_song(s) for s in new_songs]

        # Get IDs.
        old_ids_1 = [s.id for s in old_sections_1]
        old_ids_2 = [s.id for s in old_sections_2]
        free_ids = [s.id for s in free_sections]
        new_ids = [s.id for s in new_sections]

        # Randomise.
        permutation_1 = random.sample(range(n_free + n_old), n_free + n_old)
        permutation_2 = random.sample(range(n_old + n_new), n_old + n_new)
        plan = {
            'n_song_sync': n_free + n_old,
            'n_heard_before': n_old + n_new,
            'condition': condition,
            'sections': (
                [(free_ids + old_ids_1)[i] for i in permutation_1]
                + [(old_ids_2 + new_ids)[i] for i in permutation_2]
            ),
            'novelty': (
                [(['free'] * n_free + ['old'] * n_old)[i]
                 for i in permutation_1]
                + [(['old'] * n_old + ['new'] * n_new)[i]
                   for i in permutation_2]
            )
        }

        print(plan)

        # Save, overwriting existing plan if one exists.
        session.merge_json_data({'plan': plan})
        # session.save() is required for persistence
        session.save()

    @staticmethod
    def get_random_question(session):
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

        return question

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
                Score.action(session),
                FinalScore.action(
                    session=session,
                    score_message=Kuiper2020.final_score_message(session),
                    rank=Kuiper2020.rank(session)
                )
            )

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.
        next_round_number = session.get_next_round()

        # Collect actions.
        actions = []

        if next_round_number == 1:
            # Plan sections
            Kuiper2020.plan_sections(session)

            # Go to SongSync straight away.
            actions.append(Kuiper2020.next_song_sync_action(session))
        else:
            # Create a score action.
            actions.append(Score.action(session))

            # Load the heard_before offset.
            try:
                heard_before_offset = \
                    session.load_json_data()['plan']['n_song_sync'] + 1
            except KeyError as error:
                print('Missing plan key: %s' % str(error))
                return combine_actions(*actions)

            # SongSync rounds. Skip questions until Round 5.
            if next_round_number in range(2, 5):
                actions.append(Kuiper2020.next_song_sync_action(session))
            if next_round_number in range(5, heard_before_offset):
                actions.append(Kuiper2020.get_random_question(session))
                actions.append(Kuiper2020.next_song_sync_action(session))

            # HeardBefore rounds
            if next_round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(Kuiper2020.heard_before_explainer())
                actions.append(
                    Kuiper2020.next_heard_before_action(session))
            if next_round_number > heard_before_offset:
                actions.append(Kuiper2020.get_random_question(session))
                actions.append(
                    Kuiper2020.next_heard_before_action(session))

        return combine_actions(*actions)

    @staticmethod
    def next_song_sync_action(session):
        """Get next song_sync section for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            sections = plan['sections']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(sections):
            section = \
                session.section_from_any_song({'id': sections[next_round_number - 1]})
        if not section:
            print("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        result_pk = Base.prepare_result(session, section, expected_result)
        question = BooleanQuestion(
            result_id=result_pk,
            submits=True
        )
        play_config = {
            'decision_time': 15
        }
        playback = Playback([section], instructions, play_config)
        form = Form(question)
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Do you recognize this song?')
        )
        return view.action()

    @staticmethod
    def heard_before_explainer():
        """Explainer for heard-before rounds"""
        return Explainer.action(
            instruction="Bonus Rounds",
            steps=[
                Explainer.step(
                    description="Listen carefully to the music.",
                    number=1
                ),
                Explainer.step(
                    description="Did you hear the same song during previous rounds?",
                    number=2
                ),
            ])

    @staticmethod
    def next_heard_before_action(session):
        """Get next heard_before action for this session."""

        # Load plan.
        next_round_number = session.get_next_round()
        try:
            plan = session.load_json_data()['plan']
            sections = plan['sections']
            novelty = plan['novelty']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if next_round_number <= len(sections):
            section = \
                session.section_from_any_song({'id': sections[next_round_number - 1]})
        if not section:
            print("Warning: no heard_before section found")
            section = session.section_from_any_song()

        return SongBool.action(
            instruction="Did you hear this song in previous rounds?",
            session=session,
            section=section,
            expected_result=int(novelty[next_round_number - 1] == 'old')
        )

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
