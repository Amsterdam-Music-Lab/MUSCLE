import random
from .base import Base
from .views import SongSync, SongBool, FinalScore, Score, Explainer, Consent, StartSession, Playlist
from .util.questions import next_question
from .util.actions import combine_actions


class ShortLongTags(Base):
    """Rules for a experiment experiment that tests both short and long term memory with customized section selection"""

    ID = 'SHORT_LONG_TAGS'

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
            session.save()

            # Return a score and final score action
            return combine_actions(
                Score.action(session),
                FinalScore.action(
                    session=session,
                    score_message=ShortLongTags.final_score_message(session),
                    rank=ShortLongTags.rank(session)
                )
            )

        # Next round number, can be used to return different actions
        next_round_number = session.get_next_round()
        actions = []

        # Two thirds of the rounds will be song_sync, rest is heard_before
        heard_before_offset = int(session.experiment.rounds * 0.666) + 1

        if next_round_number == 1:
            # First Round, go to SongSync straight away
            actions.append(ShortLongTags.next_song_sync_action(session))
        else:
            # Create a score action
            actions.append(Score.action(session))

            # SongSync rounds
            if next_round in range(2, 3):
                actions.append(ShortLongTags.next_song_sync_action(session))

            if next_round in range(3, heard_before_offset):
                actions.append(next_question(session))
                actions.append(ShortLongTags.next_song_sync_action(session))

            # HeardBefore rounds
            if next_round_number == heard_before_offset:
                # Introduce new round type with Explainer
                actions.append(ShortLongTags.heard_before_explainer())
                actions.append(ShortLongTags.next_heard_before_action(session))

            if next_round > heard_before_offset:
                actions.append(next_question(session))
                actions.append(ShortLongTags.next_heard_before_action(session))

        return combine_actions(*actions)

    @staticmethod
    def next_song_sync_action(session, filter_by={}):
        """Get next song_sync section for this session"""

        # Only with tag_id 0 (list 1)
        filter_by = {'tag_id': 0}

        # Get section
        section = session.section_from_unused_song(filter_by)

        if not section:
            print("Warning: no section found")
            section = session.playlist.random_section(filter_by)

        return SongSync.action(
            session=session,
            section=section,
        )

    @staticmethod
    def next_heard_before_action(session, filter_by={}):
        """Get next heard_before action for this session"""

        expected_result = random.randint(0, 1) == 1

        # Get section
        section = None

        # Alternate tags between rounds
        # Not random here to make sure there is a 50/50 distribution

        # Alternately you could use a random seed approach, like:
        # - random.seed(session.id)
        # - ids = [true,true,true,true,false,false,false,false]
        # - random.choice(ids)[next_round-1-x]

        next_round_number = session.get_next_round()
        if next_round % 2 == 0:
            # Original from list 1
            filter_by['tag_id'] = 0
        else:
            # Different versions (tag_id = 1)
            # Here we assume for every song in list 1, there is at least one alternate version with tag_id 1
            filter_by['tag_id'] = 1

        if expected_result:
            # Get a random used song_id from the first series of results
            song_ids = session.song_ids()[0:int(
                session.experiment.rounds * 0.666)]
            song_id = random.choice(song_ids)

            # Get pks from sections with given filter and song_id
            pks = session.playlist.section_set.filter(
                **filter_by,
                song_id=song_id,
            ).values_list('pk', flat=True)

            if len(pks) > 0:
                section = session.playlist.section_set.get(
                    pk=random.choice(pks))

            if not section:
                print('Warning: could not find section from used song')
        else:
            section = session.section_from_unused_song(filter_by)
            if not section:
                print('Warning: could not find section from unused song')

        if not section:
            # Fallback if no section is found, get a random section
            print('Warning: no section was found')
            section = session.playlist.random_section(filter_by)

        return SongBool.action(
            instruction="Have you heard this song before in previous rounds?",
            session=session,
            section=section,
            expected_result=expected_result
        )

    @staticmethod
    def heard_before_explainer():
        """Explainer for heard-before rounds"""
        return Explainer.action(
            instruction="Bonus rounds!",
            steps=[
                Explainer.step(
                    description="Listen to the track",
                    number=1
                ),
                Explainer.step(
                    description="Indicate if you heard the song in previous rounds",
                    number=2
                ),
            ])
