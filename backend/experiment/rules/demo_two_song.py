import random
from .base import Base
from .views import Trial, FinalScore, Score, Explainer, Step, Consent, StartSession, Playlist, Question
from .views.form import Form
from .views.playback import Playback
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
        explainer = Explainer(
            instruction="How to play",
            steps=[
                Step("Read the instructions"),
                Step("Optionally start the music"),
                Step("Give an answer")
            ]).action(True)

        # 2. Consent with default text
        consent = Consent.action()

        # 3. Choose playlist
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session
        start_session = StartSession.action()

        return [
            explainer,
            consent,
            playlist,
            start_session
        ]

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
        section1 = session.playlist.section_set.all()[0]
        section2 = session.playlist.section_set.all()[1]


        # TwoSong action, with just the default options
        sections = [section1, section2]
        playback = Playback('MULTIPLE', sections)
        view = Trial(playback, None, 'Testing')
        actions.append(view.action())

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
