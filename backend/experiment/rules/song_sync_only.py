from .base import Base
from .views import SongSync, FinalScore, Score, Explainer, Consent, StartSession, Playlist
from .util.questions import next_question, DEMOGRAPHICS
from .util.actions import combine_actions


class SongSyncOnly(Base):
    """Rules for the original Hooked experiment that only tests song recognition"""

    ID = 'SONG_SYNC_ONLY'

    @staticmethod
    def first_round(experiment):
        """Create data for the first experiment rounds"""

        # 1. General explainer
        explainer = Explainer.action(
            instruction="How to play",
            steps=[
                Explainer.step(
                    description="Do you recognize this song? (try to sing along)",
                    number=1),
                Explainer.step(
                    description="Do you really know the song? (carry on singing - music will be silenced)",
                    number=2),
                Explainer.step(
                    description="Did the music restart in the right place?",
                    number=3),
                Explainer.step(
                    description="The quicker your recognize a song, the more points you can earn. Have fun!"
                )
            ])

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
                    score_message=SongSyncOnly.final_score_message(session),
                    rank=SongSyncOnly.rank(session)
                )
            )

        # Next round, can be used to return different actions
        next_round_number = session.get_next_round()
        actions = []

        song_sync_action = SongSyncOnly.next_song_sync_action(session)

        if next_round_number == 1:
            # First Round, go to SongSync straight away
            actions.append(song_sync_action)
        else:
            # Create a score action
            actions.append(Score.action(session))

            if next_round <= 3:
                # Add Question
                actions.append(next_question(session, DEMOGRAPHICS, False))
                # Add SongSync round
                actions.append(song_sync_action)

            elif next_round >= 4:
                # Add Question
                actions.append(next_question(session, DEMOGRAPHICS, True))
                # Add SongSync round
                actions.append(song_sync_action)

        return combine_actions(*actions)

    @staticmethod
    def next_song_sync_action(session):
        """Get next song_sync section for this session"""

        # Get section
        section = session.section_from_unused_song()

        if not section:
            return session.playlist.random_section()

        return SongSync.action(
            session=session,
            section=section
        )
