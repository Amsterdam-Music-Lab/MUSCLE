import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from experiment.actions.types import FeedbackInfo
from experiment.actions.final import Final
from experiment.actions.form import Form
from experiment.actions.trial import Trial
from question.utils import get_unanswered_questions
from result.score import SCORING_RULES
from session.models import Session

logger = logging.getLogger(__name__)


class BaseRules(object):
    """Base class for other rules classes"""

    contact_email = settings.CONTACT_MAIL
    counted_result_keys = []

    def __init__(self):
        self.question_series = []

    def feedback_info(self) -> FeedbackInfo:
        feedback_body = render_to_string("feedback/user_feedback.html", {"email": self.contact_email})
        return {
            # Header above the feedback form
            "header": _("Do you have any remarks or questions?"),
            # Button text
            "button": _("Submit"),
            # Body of the feedback form, can be HTML. Shown under the button
            "contact_body": feedback_body,
            # Thank you message after submitting feedback
            "thank_you": _("We appreciate your feedback!"),
            # Show a floating button on the right side of the screen to open the feedback form
            "show_float_button": False,
        }

    def calculate_score(self, result, data):
        """use scoring rule to calculate score
        If not scoring rule is defined, return None
        Override in rules file for other scoring schemes"""
        scoring_rule = SCORING_RULES.get(result.scoring_rule)
        if scoring_rule:
            return scoring_rule(result, data)
        return None

    def get_play_again_url(self, session: Session):
        participant_id_url_param = (
            f"?participant_id={session.participant.participant_id_url}"
            if session.participant.participant_id_url
            else ""
        )
        return f"/block/{session.block.slug}{participant_id_url_param}"

    def get_experiment_url(self, session: Session):
        participant_id_url_param = (
            f"?participant_id={session.participant.participant_id_url}"
            if session.participant.participant_id_url
            else ""
        )
        return f"/{session.block.phase.experiment.slug}{participant_id_url_param}"

    def get_profile_question_trials(self, session, n_questions: int = 1) -> list[Trial]:
        """Get a list of trials for questions not yet answered by the user
        Args:
            session: the current session
            n_questions: the number of questions to return, set to `None` if all questions in the blocks' question sets should be returned at once
        """
        trials = []
        question_sets = session.block.questionseries_set.all()
        if n_questions is None:
            n_questions = sum(
                question_set.questions.count() for question_set in question_sets
            )
        for question_set in question_sets:
            questions = (
                question_set.questions.order_by("?")
                if question_set.randomize
                else question_set.questions
            )
            question_iterator = get_unanswered_questions(
                session.participant, questions.all()
            )
            while len(trials) < n_questions:
                try:
                    question = next(question_iterator)
                    trials.append(
                        Trial(
                            title=_("Questionnaire"),
                            feedback_form=Form([question]),
                        )
                    )
                except StopIteration:
                    break
        if len(trials) > 1:
            for index, trial in enumerate(trials):
                trial.title = _("Questionnaire %(index)i / %(total)i") % {
                    "index": index + 1,
                    "total": len(trials),
                }
        return trials

    def has_played_before(self, session):
        """Check if the current participant has completed this game previously."""
        previous_games = Session.objects.filter(
            participant=session.participant,
            block=session.block,
            finished_at__isnull=False,
        )
        if previous_games.count():
            return True
        return False

    def calculate_intermediate_score(self, session, result):
        """process result data during a trial (i.e., between next_round calls)
        return score
        """
        return 0

    def final_score_message(self, session):
        """Create final score message for given session, base on score per result"""

        correct = 0
        total = 0

        for result in session.result_set.all():
            # if a result has score != 0, it was recognized
            if result.score:
                total += 1

                if result.score > 0:
                    # if a result has score > 0, it was identified correctly
                    correct += 1

        score_message = "Well done!" if session.final_score > 0 else "Too bad!"
        message = "You correctly identified {} out of {} recognized songs!".format(correct, total)
        return score_message + " " + message

    def rank(self, session, exclude_unfinished=True):
        """Get rank based on session score"""
        score = session.final_score
        ranks = Final.RANKS

        # Few or negative points or no score, always return lowest plastic score
        if score <= 0 or not score:
            return ranks["PLASTIC"]

        # Buckets for positive scores:
        # rank: starts percentage
        buckets = [
            # ~ stanines 1-3
            {"rank": ranks["BRONZE"], "min_percentile": 0.0},
            # ~ stanines 4-6
            {"rank": ranks["SILVER"], "min_percentile": 25.0},
            # ~ stanine 7
            {"rank": ranks["GOLD"], "min_percentile": 75.0},
            {"rank": ranks["PLATINUM"], "min_percentile": 90.0},  # ~ stanine 8
            {"rank": ranks["DIAMOND"], "min_percentile": 95.0},  # ~ stanine 9
        ]

        percentile = session.percentile_rank(exclude_unfinished)

        # Check the buckets in reverse order
        # If the percentile rank is higher than the min_percentile
        # return the rank
        for bucket in reversed(buckets):
            if percentile >= bucket["min_percentile"]:
                return bucket["rank"]

        # Default return, in case score isn't in the buckets
        return ranks["PLASTIC"]

    def validate_playlist(self, playlist: None):
        errors = []
        # Common validations across blocks
        if not playlist:
            errors.append("The block must have a playlist.")
            return errors

        sections = playlist.section_set.all()

        if not sections:
            errors.append("The block must have at least one section.")

        try:
            playlist.clean_csv()
        except ValidationError as e:
            errors += e.error_list

        return errors
