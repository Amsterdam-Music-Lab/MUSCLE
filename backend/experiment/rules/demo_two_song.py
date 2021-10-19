import random
from .base import Base
from .views import TwoSong, FinalScore, Score, Explainer, Consent, StartSession, Playlist, Question
from .util.questions import next_question, DEMOGRAPHICS
from .util.actions import combine_actions


class DemoTwoSong(Base):
    """
    Demonstrate new view/widgets functionality:
    - TwoSong
    - ResultQuestion
    """

    ID = 'DEMO_TWO_SONG'

    @staticmethod
    def first_round(experiment):
        """Create data for the first experiment rounds"""

        # 1. General explainer
        explainer = Explainer.action(
            instruction="How to play",
            steps=[
                Explainer.step(
                    description="Read the instructions",
                    number=1),
                Explainer.step(
                    description="Optionally start the music",
                    number=2),
                Explainer.step(
                    description="Give an answer",
                    number=3),
            ])

        # 2. Consent with default text
        consent = Consent.action()

        # 3. Choose playlist
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session
        start_session = StartSession.action()

        return combine_actions(
            explainer,
            consent,
            playlist,
            start_session
        )

    @staticmethod
    def next_round(session):
        """Get action data for the next round"""

        # If the number of results equals the number of experiment.rounds
        # Close the session and return data for the final_score view
        if session.rounds_complete():
            # Finish session
            session.finish()

            # Example answer stats
            print("Answered questions: {}".format(
                session.answered_questions()))
            print("Skipped questions: {}".format(session.skipped_questions()))

            # Penalty/Bonus for (not) answering questions
            session.final_score += session.question_bonus(
                bonus=100,
                skip_penalty=5
            )

            session.save()

            # Return a score and final score action
            return combine_actions(
                Score.action(session),
                FinalScore.action(
                    session=session,
                    score_message=DemoTwoSong.final_score_message(session),
                    rank=DemoTwoSong.rank(session)
                )
            )

        # Next round, can be used to return different actions
        next_round_number = session.get_next_round()
        actions = []

        # Get sections for the next round
        section1 = DemoTwoSong.next_section(session)
        section2 = DemoTwoSong.next_section(session)

        # Default TwoSong options
        two_song_options = {
            'session': session,
            'section1': section1,
            'section2': section2,
            'introduction': "Listen to these musical fragments:",
            'instruction': "Which of the fragments sounds catchier to you?",
            'expected_result': 2,  # 1 or 2
        }

        # Build up this experiment per round
        if next_round_number == 1:
            # TwoSong action, with just the default options
            actions.append(
                DemoTwoSong.create_two_song_action(two_song_options))

        elif next_round_number == 2:
            # TwoSong action, with modified parameters
            actions.append(
                DemoTwoSong.create_two_song_action(two_song_options,
                                                   section1_color="pink",
                                                   section1_label="I",
                                                   section2_color="yellow",
                                                   section2_label="II",
                                                   button1_label="Snippet I",
                                                   button2_label="Snippet II",
                                                   button1_color="red",
                                                   button2_color="blue",
                                                   introduction="",
                                                   instruction="Parameters are customizable",
                                                   ))

        elif next_round >= 3:
            # Default TwoSong action
            actions.append(
                DemoTwoSong.create_two_song_action(two_song_options))

        # Example for alternate question introduction using the Explainer
        if next_round_number == 3:
            actions.insert(0, Explainer.action(
                instruction="How to play",
                steps=[
                    Explainer.step(
                        "Click on the play buttons to listen to a short fragment", number=1),
                    Explainer.step(
                        "Let us know which of the fragments sounds catchier to you", number=2)
                ],
                button_label="Continue"
            ))

        if next_round > 1:
            # Add a Profile Question to the actions list
            actions.insert(0, next_question(session, DEMOGRAPHICS, True))

        return combine_actions(*actions)

    @staticmethod
    def create_two_song_action(options, **kwargs):
        """Create a TwoSong actions, based on the given options, with optional kwargs overrides"""
        for key, value in kwargs.items():
            options[key] = value
        return TwoSong.action(**options)

    @staticmethod
    def next_section(session, filter_by={}):
        """Get next section for given session"""
        section = session.section_from_unused_song(filter_by)
        return section if section else session.section_from_any_song(filter_by)

    @staticmethod
    def calculate_score(session, data):
        """Calculate score depending on view"""

        # excluded SongSync and SongBool here
        if data['view'] == TwoSong.ID:
            score = TwoSong.calculate_score(session, data)

            # Round the score, to prevent view artifacts
            return round(score)

        return None
