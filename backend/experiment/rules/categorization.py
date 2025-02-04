import random

from django.utils import timezone
from django.template.loader import render_to_string
from django.db.models import Avg

from experiment.actions.form import Form, ChoiceQuestion
from experiment.actions.styles import ButtonStyle, ColorScheme
from experiment.actions import Explainer, Score, Trial, Final
from experiment.actions.wrappers import two_alternative_forced
from session.models import Session

from .base import BaseRules

SCORE_AVG_MIN_TRAINING = 0.8


class Categorization(BaseRules):
    ID = "CATEGORIZATION"
    default_consent_file = "consent/consent_categorization.html"

    def __init__(self):
        self.question_series = [
            {
                "name": "Categorization",
                "keys": ["dgf_age", "dgf_gender_reduced", "dgf_native_language", "dgf_musical_experience"],
                "randomize": False,
            },
        ]

    def get_intro_explainer(self):
        return Explainer(
            instruction="This is a listening experiment in which you have to respond to short sound sequences.",
            steps=[],
            button_label="Ok",
        )

    def next_round(self, session: Session):
        json_data = session.json_data

        if not json_data.get("phase"):
            actions = [self.get_intro_explainer()]
            questions = self.get_open_questions(session)
            if questions:
                actions.extend(questions)
            json_data = self.plan_experiment(session)
            return actions

        # Calculate round number from passed training rounds
        rounds_passed = session.get_rounds_passed() - int(json_data["training_rounds"])
        # Change phase to enable collecting results of second half of training-1
        if session.get_rounds_passed() == 10:
            json_data["phase"] = "training-1B"
            session.save_json_data(json_data)
            session.save()

        if rounds_passed == 0:
            # Check if participants wants to exit after failed traning
            profiles = session.participant.profile()
            for profile in profiles:
                # Delete results and json from session and exit
                if profile.given_response == "aborted":
                    session.result_set.all().delete()
                    json_data = {"phase": "ABORTED", "training_rounds": json_data["training_rounds"]}
                    session.save_json_data(json_data)
                    session.save()
                    profile.delete()
                    final_message = render_to_string("final/categorization_final.html")
                    final = Final(
                        session=session,
                        final_text="Thanks for your participation!" + final_message,
                    )
                    return final
            # Prepare sections for next phase
            json_data = self.plan_phase(session)

        if "training" in json_data["phase"]:
            if rounds_passed == 0:
                explainer2 = Explainer(
                    instruction="The experiment will now begin. Please don't close the browser during the experiment. You can only run it once. Click to start a sound sequence.",
                    steps=[],
                    button_label="Ok",
                )
                trial = self.next_trial_action(session)
                return [explainer2, trial]

            # Get next training action
            elif rounds_passed < len(json_data["sequence"]):
                return self.get_trial_with_feedback(session)

            # Training phase completed, get the results
            training_rounds = int(json_data["training_rounds"])

            if training_rounds == 0:
                this_results = session.result_set.filter(comment="training-1B")
            elif training_rounds == 20:
                this_results = session.result_set.filter(comment="training-2")
            elif training_rounds == 30:
                this_results = session.result_set.filter(comment="training-3")
            # calculate the score for this sequence
            score_avg = this_results.aggregate(Avg("score"))["score__avg"]

            # End of training?
            if score_avg >= SCORE_AVG_MIN_TRAINING:
                json_data["phase"] = "testing"
                json_data["training_rounds"] = session.get_rounds_passed()
                session.save_json_data(json_data)
                session.save()
                explainer = Explainer(
                    instruction="You are entering the main phase of the experiment. From now on you will only occasionally get feedback on your responses. Simply try to keep responding to the sound sequences as you did before.",
                    steps=[],
                    button_label="Ok",
                )
            else:
                # Update passed training rounds for calc round_number
                json_data["training_rounds"] = session.get_rounds_passed()
                session.save_json_data(json_data)
                session.save()

                # Failed the training? exit experiment
                if json_data["training_rounds"] == 40:
                    # Clear group from session for reuse
                    end_data = {
                        "phase": "FAILED_TRAINING",
                        "training_rounds": json_data["training_rounds"],
                        "assigned_group": json_data["assigned_group"],
                        "button_colors": json_data["button_colors"],
                        "pair_colors": json_data["pair_colors"],
                    }
                    session.save_json_data(end_data)
                    session.final_score = 0
                    session.save()
                    profiles = session.participant.profile()
                    for profile in profiles:
                        # Delete failed_training tag from profile
                        if profile.question_key == "failed_training":
                            profile.delete()
                    final_message = render_to_string("final/categorization_final.html")
                    final = Final(
                        session=session,
                        final_text="Thanks for your participation!" + final_message,
                    )
                    return final
                else:
                    # Show continue to next training phase or exit option
                    explainer = Trial(title="Training failed", feedback_form=Form([repeat_training_or_quit]))

            feedback = self.get_feedback(session)
            return [feedback, explainer]

        elif json_data["phase"] == "testing":
            if rounds_passed < len(json_data["sequence"]):
                # Determine wether this round has feedback
                if rounds_passed in json_data["feedback_sequence"]:
                    return self.get_trial_with_feedback(session)
                return self.next_trial_action(session)

            # Testing phase completed get results
            this_results = session.result_set.filter(comment="testing")

            # Calculate percentage of correct response to training stimuli
            final_score = 0
            for result in this_results:
                if "T" in result.section.song.name and result.score == 1:
                    final_score += 1
            score_percent = 100 * (final_score / 30)

            ranks = Final.RANKS

            # assign rank based on percentage of correct response to training stimuli
            if score_percent == 100:
                rank = ranks["PLATINUM"]
                final_text = "Congratulations! You did great and won a platinum medal!"
            elif score_percent >= 80:
                rank = ranks["GOLD"]
                final_text = "Congratulations! You did great and won a gold medal!"
            elif score_percent >= 60:
                rank = ranks["SILVER"]
                final_text = "Congratulations! You did very well and won a silver medal!"
            else:
                rank = ranks["BRONZE"]
                final_text = "Congratulations! You did well and won a bronze medal!"

            # calculate the final score for the entire test sequence
            # final_score = sum([result.score for result in training_results])
            end_data = {
                "phase": "FINISHED",
                "training_rounds": json_data["training_rounds"],
                "assigned_group": json_data["assigned_group"],
                "button_colors": json_data["button_colors"],
                "pair_colors": json_data["pair_colors"],
                "group": json_data["group"],
            }
            session.save_json_data(end_data)
            session.finish()
            session.final_score = final_score
            session.save()
            profiles = session.participant.profile()
            for profile in profiles:
                # Delete failed_training tag from profile
                if profile.question_key == "failed_training":
                    profile.delete()
            final_message = render_to_string("final/categorization_final.html")
            final = Final(
                session=session,
                final_text=final_text + final_message,
                total_score=round(score_percent),
                rank=rank,
                points="% correct",
            )
            return final

    def plan_experiment(self, session):
        """
        Randomly assign one of four (equal sized) groups to participants
        S1 = Same direction, Pair 1
        S2 = Same direction, Pair 2
        C1 = Crossed direction, Pair 1
        C2 = Crossed direction, Pair 2
        BLUE / ORANGE = Correct response for Pair 1A, Pair 2A
        """

        # Check for unfinished sessions older then 24 hours caused by closed browser
        all_sessions = (
            session.block.session_set.filter(finished_at=None)
            .filter(started_at__lte=timezone.now() - timezone.timedelta(hours=24))
            .exclude(json_data__contains="ABORTED")
            .exclude(json_data__contains="FAILED_TRAINING")
            .exclude(json_data__contains="CLOSED_BROWSER")
        )
        for closed_session in all_sessions:
            # Release the group for assignment to a new participant
            closed_json_data = {"phase": "CLOSED_BROWSER"}
            # Delete results
            closed_session.save_json_data(closed_json_data)
            closed_session.result_set.all().delete()
            closed_session.save()

        # Count sessions per assigned group
        used_groups = [
            session.block.session_set.filter(json_data__contains="S1").count(),
            session.block.session_set.filter(json_data__contains="S2").count(),
            session.block.session_set.filter(json_data__contains="C1").count(),
            session.block.session_set.filter(json_data__contains="C2").count(),
        ]

        # Check wether a group falls behind in the count
        if max(used_groups) - min(used_groups) > 1:
            # assign the group that falls behind
            group_index = used_groups.index(min(used_groups))
            if group_index == 0:
                group = "S1"
            elif group_index == 1:
                group = "S2"
            elif group_index == 2:
                group = "C1"
            elif group_index == 3:
                group = "C2"
        else:
            # Assign a random group
            group = random.choice(["S1", "S2", "C1", "C2"])
        # Assign a random correct response color for 1A, 2A
        stimuli_a = random.choice(["BLUE", "ORANGE"])
        # Determine which button is orange and which is blue
        button_order = random.choice(
            [ColorScheme.NEUTRAL.value, ColorScheme.NEUTRAL_INVERTED.value]
        )
        # Set expected resonse accordingly
        ph = "___"  # placeholder
        if button_order == "neutral" and stimuli_a == "BLUE":
            choices = {"A": ph, "B": ph}
        elif (
            button_order == ColorScheme.NEUTRAL_INVERTED.value and stimuli_a == "ORANGE"
        ):
            choices = {"A": ph, "B": ph}
        else:
            choices = {"B": ph, "A": ph}
        if group == "S1":
            assigned_group = "Same direction, Pair 1"
        elif group == "S2":
            assigned_group = "Same direction, Pair 2"
        elif group == "C1":
            assigned_group = "Crossed direction, Pair 1"
        else:
            assigned_group = "Crossed direction, Pair 2"
        if button_order == ColorScheme.NEUTRAL.value:
            button_colors = "Blue left, Orange right"
        else:
            button_colors = "Orange left, Blue right"
        if stimuli_a == "BLUE":
            pair_colors = "A = Blue, B = Orange"
        else:
            pair_colors = "A = Orange, B = Blue"
        json_data = {
            "phase": "training",
            "training_rounds": "0",
            "assigned_group": assigned_group,
            "button_colors": button_colors,
            "pair_colors": pair_colors,
            "group": group,
            "stimuli_a": stimuli_a,
            "button_order": button_order,
            "choices": choices,
        }
        session.save_json_data(json_data)
        session.save()

        return json_data

    def plan_phase(self, session):
        json_data = session.json_data
        if "training" in json_data["phase"]:
            # Retrieve training stimuli for the assigned group
            if json_data["group"] == "S1":
                sections = session.playlist.section_set.filter(
                    group="SAME", tag__contains="1", song__artist__contains="Training"
                )
            elif json_data["group"] == "S2":
                sections = session.playlist.section_set.filter(
                    group="SAME", tag__contains="2", song__artist__contains="Training"
                )
            elif json_data["group"] == "C1":
                sections = session.playlist.section_set.filter(
                    group="CROSSED", tag__contains="1", song__artist__contains="Training"
                )
            elif json_data["group"] == "C2":
                sections = session.playlist.section_set.filter(
                    group="CROSSED", tag__contains="2", song__artist__contains="Training"
                )
            # Generate randomized sequence for the testing phase
            section_sequence = []
            # Add 10 x 2 training stimuli
            if int(json_data["training_rounds"]) == 0:
                new_rounds = 10
                json_data["phase"] = "training-1A"
            elif int(json_data["training_rounds"]) == 20:
                json_data["phase"] = "training-2"
                new_rounds = 5
            else:
                json_data["phase"] = "training-3"
                new_rounds = 5
            for _ in range(0, new_rounds):
                section_sequence.append(sections[0].song_id)
                section_sequence.append(sections[1].song_id)
            random.shuffle(section_sequence)
            json_data["sequence"] = section_sequence

        else:
            # Retrieve test & training stimuli for the assigned group
            if json_data["group"] == "S1":
                training_sections = session.playlist.section_set.filter(
                    group="SAME", tag__contains="1", song__artist__contains="Training"
                )
                test_sections = session.playlist.section_set.filter(group="SAME", tag__contains="1").exclude(
                    song__artist__contains="Training"
                )
            elif json_data["group"] == "S2":
                training_sections = session.playlist.section_set.filter(
                    group="SAME", tag__contains="2", song__artist__contains="Training"
                )
                test_sections = session.playlist.section_set.filter(group="SAME", tag__contains="2").exclude(
                    song__artist__contains="Training"
                )
            elif json_data["group"] == "C1":
                training_sections = session.playlist.section_set.filter(
                    group="CROSSED", tag__contains="1", song__artist__contains="Training"
                )
                test_sections = session.playlist.section_set.filter(group="CROSSED", tag__contains="1").exclude(
                    song__artist__contains="Training"
                )
            elif json_data["group"] == "C2":
                training_sections = session.playlist.section_set.filter(
                    group="CROSSED", tag__contains="2", song__artist__contains="Training"
                )
                test_sections = session.playlist.section_set.filter(group="CROSSED", tag__contains="2").exclude(
                    song__artist__contains="Training"
                )
            # Generate randomized sequence for the testing phase
            section_sequence = []
            # Add 15 x 2 training stimuli
            for _ in range(0, 15):
                section_sequence.append(training_sections[0].song_id)
                section_sequence.append(training_sections[1].song_id)
            # add 5 x 10 test stimuli
            length = len(test_sections)
            for _ in range(0, 5):
                for stimulus in range(length):
                    section_sequence.append(test_sections[stimulus].song_id)
            random.shuffle(section_sequence)
            # Randomly choose 2 x 10 training stimuli for feedback
            sequence_length = len(section_sequence)
            sequence_a = []
            sequence_b = []
            for stimulus in range(sequence_length - 1):
                if section_sequence[stimulus] == training_sections[0].song_id:
                    sequence_a.append((stimulus + 1))
                elif section_sequence[stimulus] == training_sections[1].song_id:
                    sequence_b.append((stimulus + 1))
            random.shuffle(sequence_a)
            random.shuffle(sequence_b)
            feedback_sequence = sequence_a[0:10] + sequence_b[0:10]
            json_data["feedback_sequence"] = feedback_sequence
            json_data["sequence"] = section_sequence

        session.save_json_data(json_data)
        session.save()

        return json_data

    def get_feedback(self, session):
        last_score = session.last_score()

        if session.last_result().given_response == "TIMEOUT":
            icon = "fa-question"
        elif last_score == 1:
            icon = "fa-face-smile"
        elif last_score == 0:
            icon = "fa-face-frown"
        else:
            pass  # throw error

        return Score(session, icon=icon, timer=1, title=" ")

    def get_trial_with_feedback(self, session):
        score = self.get_feedback(session)
        trial = self.next_trial_action(session)

        return [score, trial]

    def next_trial_action(self, session):
        """
        Get the next action for the experiment
        """
        json_data = session.json_data

        # Retrieve next section in the sequence
        rounds_passed = session.get_rounds_passed() - int(json_data["training_rounds"])
        sequence = json_data["sequence"]
        this_section = sequence[rounds_passed]
        section = session.playlist.get_section(song_ids=[this_section])
        # Determine expected response
        if section.tag == "1A" or section.tag == "2A":
            expected_response = "A"
        else:
            expected_response = "B"

        choices = json_data["choices"]
        config = {"listen_first": True, "auto_advance": True, "auto_advance_timer": 2500, "time_pass_break": False}
        style = [json_data["button_order"]]
        trial = two_alternative_forced(
            session,
            section,
            choices,
            expected_response,
            style=style,
            comment=json_data["phase"],
            scoring_rule="CORRECTNESS",
            title=self.get_title(session),
            config=config,
        )
        return trial

    def get_title(self, session):
        json_data = session.json_data
        rounds_passed = session.get_rounds_passed() - int(json_data["training_rounds"]) + 1
        return f"Round {rounds_passed} / {len(json_data['sequence'])}"


repeat_training_or_quit = ChoiceQuestion(
    key="failed_training",
    view="BUTTON_ARRAY",
    question="You seem to have difficulties reacting correctly to the sound sequences. Is your audio on? If you want to give it another try, click on Ok.",
    choices={"continued": "OK", "aborted": "Exit"},
    submits=True,
    is_skippable=False,
    style=[ButtonStyle.LARGE_GAP, ButtonStyle.LARGE_TEXT, ColorScheme.BOOLEAN],
)
