import random
import logging

from django.utils.translation import gettext_lazy as _

from experiment.actions.utils import (
    final_action_with_optional_button,
    render_feedback_trivia,
)
from experiment.actions import Trial, Explainer, Step
from experiment.actions.playback import Autoplay
from experiment.actions.form import ChoiceQuestion, Form

from result.utils import prepare_result
from section.models import Playlist
from session.models import Session

from .practice import Practice

logger = logging.getLogger(__name__)

STIMULI = {
    'practice': {
        'metric': {
            'standard': '4 1 1 1 1 3 1',
            'deviant': '1 1 2 4 2 2',
        },
        'nonmetric': {
            'standard': '4.5  1 1  3.5  3.5',
            'deviant': '4.5 1 1.4  1.4 1 1.4'
        }
    },
    'nonmetric':  {
        'standard': [
            '1 1  3.5  4.5  3.5',
            '1 3.5  1.4  4.5  1.4',
            '1 3.5  1.4  3.5  1.4 1',
            '3.5  1.4  3.5  1.4  1 1',
            '4.5  1.4 1 3.5  1 1',
            '1 3.5 1 4.5  1 1 1',
            '1.4  3.5  3.5  1 1  1 1',
            '1.4 1 4.5 1 1.4  1 1',
            '3.5  1 1  4.5  1 1 1'
        ],
        'deviant': [
            '1.4  3.5  1.4  4.5 1',
            '3.5  3.5 1 4.5 1',
            '1 1.4  1.4 1 4.5  1.4',
            '1 1.4  4.5  1 1  3.5',
            '1 1.4 1 1.4  3.5  3.5',
            '1.4  1.4 1 1.4  4.5 1',
            '1 1  3.5  1.4 1 3.5 1',
            '1 4.5  1 1  3.5  1 1',
            '1.4 1 1.4  3.5  1.4  1 1'
        ]
    },
    'metric': {
        'standard': [
            '3 1 4 2 2',
            '4 3 1 2 2',
            '2 1 1 2 2 4',
            '2 2 2 1 1 4',
            '4 2 2 1 1 2',
            '1 1 2 2 1 1 4',
            '1 1 2 3 1 2 2',
            '2 2 1 1 1 1 4',
            '3 1 4 1 1 1 1'
        ],
        'deviant': [
            '2 2 4 1 3',
            '3 1 4 1 3',
            '1 1 2 3 1 4',
            '2 1 1 1 3 4',
            '2 2 3 1 1 3',
            '3 1 1 3 2 2',
            '1 1 2 3 1 1 3',
            '2 1 1 3 1 1 3',
            '4 2 2 1 1 1 1'
        ]
    }
}


class RhythmDiscrimination(Practice):
    ID = 'RHYTHM_DISCRIMINATION'
    first_condition = "different"
    first_condition_i18n = _("DIFFERENT")
    second_condition = "same"
    second_condition_i18n = _("SAME")

    def next_round(self, session):

        if session.get_rounds_passed() == 0:
            self.plan_stimuli(session)

        if not session.json_data.get("practice_done"):
            return self.next_practice_round()

        else:
            plan = session.json_data.get("plan")
            if not plan:
                print("No stimulus plan found in session json_data")
                return None

            if len(plan) == session.get_rounds_passed():
                return [self.finalize_block(session)]
            return self.get_next_trial(session)

    def get_condition(self, session):
        plan = session.json_data.get("plan")
        round_number = session.get_rounds_passed()
        return plan[round_number]

    def get_next_trial(self, session):
        """
        Get the next trial action, depending on the round number
        """
        condition = self.get_condition(session)

        try:
            section = (
                session.playlist.section_set.filter(
                    song__name__startswith=condition["rhythm"]
                )
                .filter(tag=condition["tag"])
                .get(group=condition["group"])
            )
        except:
            return None

        expected_response = (
            self.first_condition if condition["group"] == "0" else self.second_condition
        )
        key = "same_or_different"
        question = ChoiceQuestion(
            key=key,
            question=_("Is the third rhythm the SAME or DIFFERENT?"),
            choices={
                self.first_condition: self.first_condition_i18n,
                self.second_condition: self.second_condition_i18n,
            },
            view="BUTTON_ARRAY",
            result_id=prepare_result(
                key,
                session,
                expected_response=expected_response,
                scoring_rule="CORRECTNESS",
            ),
            submits=True,
        )
        form = Form([question])
        playback = Autoplay([section])

        return Trial(
            playback=playback,
            feedback_form=form,
            title=_("Rhythm discrimination: %s" % (self.get_title(session))),
            config={"listen_first": True, "response_time": section.duration + 0.5},
        )

    def get_title(self, session):
        round_number = session.get_rounds_passed()
        plan = session.json_data.get("plan")
        return _("trial %(index)d of %(total)d") % (
            {"index": round_number - 4, "total": len(plan) - 4}
        )

    def plan_stimuli(self, session):
        """select 60 stimuli, of which 30 are standard, 30 deviant.
        rhythm refers to the type of rhythm,
        tag refers to the tempo,
        group refers to the condition (0 is deviant, 1 is standard)
        """
        metric = STIMULI["metric"]
        nonmetric = STIMULI["nonmetric"]
        tempi = [150, 160, 170, 180, 190, 200]
        tempi = [str(t) for t in tempi]
        metric_deviants = [
            {"rhythm": m, "tag": random.choice(tempi), "group": "0"}
            for m in metric["deviant"]
        ]
        metric_standard = [
            {"rhythm": m, "tag": random.choice(tempi), "group": "1"}
            for m in metric["standard"]
        ]
        nonmetric_deviants = [
            {"rhythm": m, "tag": random.choice(tempi), "group": "0"}
            for m in nonmetric["deviant"]
        ]
        nonmetric_standard = [
            {"rhythm": m, "tag": random.choice(tempi), "group": "1"}
            for m in nonmetric["standard"]
        ]
        practice = [
            {
                "rhythm": STIMULI["practice"]["metric"]["standard"],
                "tag": random.choice(tempi),
                "group": "1",
            },
            {
                "rhythm": STIMULI["practice"]["metric"]["deviant"],
                "tag": random.choice(tempi),
                "group": "0",
            },
            {
                "rhythm": STIMULI["practice"]["nonmetric"]["standard"],
                "tag": random.choice(tempi),
                "group": "1",
            },
            {
                "rhythm": STIMULI["practice"]["nonmetric"]["deviant"],
                "tag": random.choice(tempi),
                "group": "0",
            },
        ]
        block = (
            metric_deviants + metric_standard + nonmetric_deviants + nonmetric_standard
        )
        random.shuffle(block)
        plan = practice + block
        session.save_json_data({"plan": plan})
        session.save()

    def get_intro_explainer(self) -> Explainer:
        return Explainer(
            instruction=_(
                "In this test you will hear the same rhythm twice. After that, you will hear a third rhythm."
            ),
            steps=[
                Step(
                    _(
                        "Your task is to decide whether this third rhythm is the SAME as the first two rhythms or DIFFERENT."
                    )
                ),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(
                    _(
                        "This test will take around 6 minutes to complete. Try to stay focused for the entire test!"
                    )
                ),
            ],
            step_numbers=True,
            button_label="Ok",
        )

    def get_feedback_explainer(self, session):
        correct_response, is_correct = self.get_condition_and_correctness(session)
        if is_correct:
            instruction = _(
                "The third rhythm is the %(correct_response)s. Your response was CORRECT."
            ) % {"correct_response": correct_response}
        else:
            instruction = _(
                "The third rhythm is the %(correct_response)s. Your response was INCORRECT."
            ) % {"correct_response": correct_response}
        return Explainer(
            instruction=instruction, steps=[], button_label=_("Next fragment")
        )

    def finalize_block(session):
        # we had 4 practice trials and 60 experiment trials
        percentage = (
            sum([res.score for res in session.result_set.all()])
            / session.result_set.count()
        ) * 100
        session.finish()
        session.save()
        feedback = _("Well done! You've answered {} percent correctly!").format(
            percentage
        )
        trivia = _(
            "One reason for the \
            weird beep-tones in this test (instead of some nice drum-sound) is that it is used very often\
            in brain scanners, which make a lot of noise. The beep-sound helps people in the scanner \
            to hear the rhythm really well."
        )
        final_text = render_feedback_trivia(feedback, trivia)
        return final_action_with_optional_button(session, final_text)

    def practice_successful(self, session: Session) -> bool:
        """Check if practice was successful: at least one answer correct"""
        results = session.last_n_results(n_results=4)
        return any([r.score > 0 for r in results])

    def validate_playlist(self, playlist: Playlist):
        errors = []
        errors += super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        if not sections.count():
            return errors
        if sections.count() != 720:
            errors.append("The block needs a playlist with 720 sections")
        tags, groups = zip(*[(s.tag, s.group) for s in sections])
        try:
            tag_numbers = sorted(list(set([int(t) for t in tags])))
            if tag_numbers != [150, 160, 170, 180, 190, 200]:
                errors.append("Tags should have values 150, 160, 170, 180, 190, 200")
        except:
            errors.append("The sections should have integer tags")
        try:
            group_numbers = sorted(list(set([int(g) for g in groups])))
            if group_numbers != [0, 1]:
                errors.append("Groups should have values 0, 1")
        except:
            errors.append("The sections should have integer groups")

        def pattern_error(pattern: str) -> str:
            return f"There should be 12 sections with pattern {pattern}"

        metric_standard = STIMULI["metric"]["standard"]
        for m in metric_standard:
            if sections.filter(song__name__startswith=m).count() != 12:
                errors.append(pattern_error(m))
        metric_deviant = STIMULI["metric"]["deviant"]
        for m in metric_deviant:
            if sections.filter(song__name__startswith=m).count() != 12:
                errors.append(pattern_error(m))
        nonmetric_standard = STIMULI["nonmetric"]["standard"]
        for n in nonmetric_standard:
            if sections.filter(song__name__startswith=n).count() != 12:
                errors.append(pattern_error(n))
        nonmetric_deviant = STIMULI["nonmetric"]["deviant"]
        for n in nonmetric_deviant:
            if sections.filter(song__name__startswith=n).count() != 12:
                errors.append(pattern_error(n))

        return errors
