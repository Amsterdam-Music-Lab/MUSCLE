import random
from .base import Base
from .views import TwoAlternativeForced, FinalScore, Score, Explainer, Consent, StartSession, Playlist, Question
from .util.questions import next_question, DEMOGRAPHICS
from .util.actions import combine_actions


class DemoTAF(Base):
    """
    Demonstrate new view/widgets functionality:
    - TwoAlternativeForced
    - ResultQuestion
    """

    ID = 'DEMO_TAF'

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
                Explainer.step(
                    description="Are you certain about your answer?",
                    number=4),
                Explainer.step(
                    description="The quicker your give an answer, the more points you can earn. Have fun!"
                )
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
                    score_message=DemoTAF.final_score_message(session),
                    rank=DemoTAF.rank(session)
                )
            )

        # Next round, can be used to return different actions
        next_round_number = session.get_next_round()
        actions = []

        # Get a section for the next round
        section = DemoTAF.next_section(session)

        # Default TAF options
        taf_options = {
            'session': session,
            'section': section,
            'auto_play': False,
            'introduction': "Play the song and answer the question:",
            'instruction': "What is the music genre of this song?",
            'expected_result': 2,  # 1 or 2
            'button1_label': "Rock and Roll",
            'button1_color': "blue",
            'button2_label': "Classical",
            'button2_color': "teal",
            # Eliminate the preload countdown
            'ready_time': 0,
            'ready_message': '',

            # Stop auto advance (so give user unlimited time to give answer)
            'auto_advance': False,

            # Listen first before buttons become active
            # 'listen_first': True,

            # Skip any subsequent actions when time has passed (e.g. skip certainty question)
            # 'time_pass_break': True,
        }

        # Build up this experiment per round
        if next_round_number == 1:
            # TwoAlternativeForced action, with just the default options
            actions.append(DemoTAF.create_taf_action(taf_options))

            # Certainty question
            actions.append(Question.certainty_radios(
                # You can choose your own 'key' value, which is stored with the question data
                # This is useful to identify the question type during the data analysis
                key="certainty",
                # make sure to specify it as a result-question (instead of the default profile-questions)
                view=Question.ID_RESULT_QUESTION
            ))

        elif next_round >= 2:
            # Example data
            expected_result = random.randint(1, 2)
            # Or use the section group_id to get an expected result, e.g.
            # expected_result = 1 if section.group_id == 1 else 2

            other_composers = ['Wolfgang Amadeus Mozart', 'Johann Sebastian Bach',
                               'Joseph Haydn', 'Claude Debussy', 'Frédéric Chopin', 'Johannes Brahms']
            random_composer = random.sample(other_composers, 1)

            # Create a score action
            actions.append(Score.action(session, include_section=False))

            # TwoAlternativeForced action, with modified parameters
            actions.append(DemoTAF.create_taf_action(
                taf_options,
                auto_play=random.randint(0, 1) == 1,
                introduction="Listen to the song",
                instruction="Who composed this song?",
                button1_label=section.artist if expected_result == 1 else random_composer,
                button2_label=section.artist if expected_result == 2 else random_composer,
                expected_result=expected_result,
            ))

            # Certainty question
            actions.append(Question.certainty_radios(
                key="certainty",
                # make sure to specify it as a result-question (instead of the default profile-questions)
                view=Question.ID_RESULT_QUESTION
            ))

        # Example for alternate question introduction using the Explainer
        if next_round_number == 3:
            actions.insert(1, Explainer.action(
                instruction="How to play",
                steps=[
                    Explainer.step("Listen to the song"),
                    Explainer.step(
                        "Indicate if the music is a 3/4 or 4/4 time")
                ],
                button_label="Start question"
            ))

        if next_round > 1:
            # Add a Profile Question to the actions actions list (after the score action at position 0)
            actions.insert(1, next_question(session, DEMOGRAPHICS, True))

        return combine_actions(*actions)

    @staticmethod
    def create_taf_action(options, **kwargs):
        """Create a TAF actions, based on the given options, with optional kwargs overrides"""
        for key, value in kwargs.items():
            options[key] = value
        return TwoAlternativeForced.action(**options)

    @staticmethod
    def next_section(session, filter_by={}):
        """Get next section for given session"""
        section = session.section_from_unused_song(filter_by)
        return section if section else session.section_from_any_song(filter_by)

    @staticmethod
    def calculate_score(session, data):
        """Calculate score depending on view"""

        # excluded SongSync and SongBool here
        if data['view'] == TwoAlternativeForced.ID:
            score = TwoAlternativeForced.calculate_score(session, data)

            # Boost score by certainty
            try:

                question = data['question']
                if question['key'] == 'certainty':
                    # Multiplying the given score - which is already positive (correct) or negative (incorrect)
                    # gives a nice score boost based on the given certainty

                    if question['answer'] == '1':
                        # guessed
                        score *= 0.5
                    elif question['answer'] == '2':
                        # think
                        score *= 1
                    elif question['answer'] == '3':
                        # sure
                        score *= 1.5

            except KeyError:
                # Do nothing
                score = 1 * score

            # Round the score, to prevent view artifacts
            return round(score)

        return None
