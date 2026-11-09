import logging
from typing import Optional, Union

from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from experiment.actions.form import Form
from experiment.actions.trial import Trial
from experiment.actions.types import FeedbackInfo
from question.utils import get_unanswered_questions
from result.models import Result
from result.score import SCORING_RULES
from result.utils import prepare_profile_result
from section.models import Playlist
from session.models import Session

logger = logging.getLogger(__name__)


class BaseRules(object):
    """Base class for other rules classes"""

    contact_email = settings.CONTACT_MAIL
    counted_result_identifiers = []

    def feedback_info(self) -> FeedbackInfo:
        """
        Return info to shown to the user if they are invited to give feedback
        """
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

    def calculate_score(
        self, result: Result, data: dict
    ) -> Optional[Union[int, float]]:
        """Use scoring rule to calculate score.

        The function uses the result's scoring rule, if configured, otherwise, returns `None`.

        Args:
            result: the Result object for which to calculate the score
            data: the data of the participant's response

        """
        scoring_rule = SCORING_RULES.get(result.scoring_rule)
        if scoring_rule:
            return scoring_rule(result, data)
        return None

    def get_profile_question_trials(
        self, session: Session, n_questions: int = 1
    ) -> list[Trial]:
        """Get a list of trials for questions not yet answered by the user

        Args:
            session: the current session
            n_questions: the number of questions to return, set to `None` if all questions in the blocks' question lists should be returned at once

        Returns:
            list of `Trial` actions with unanswered questions
        """
        trials = []
        question_lists = session.block.questionlist_set.all()
        if n_questions is None:
            n_questions = sum(ql.questions.count() for ql in question_lists)
        for ql in question_lists:
            questions = (
                ql.questions.order_by("?") if ql.randomize else ql.get_questions()
            )
            question_iterator = get_unanswered_questions(
                session.participant, questions.all()
            )
            while len(trials) < n_questions:
                try:
                    question_obj = next(question_iterator)
                    profile_result = prepare_profile_result(
                        question_obj.identifier, session.participant
                    )
                    question = question_obj.convert_to_action()
                    question.result_id = profile_result.id
                    feedback_form = (
                        Form([question], skip_button=None)
                        if question_obj.is_skippable
                        else Form([question])
                    )
                    trials.append(
                        Trial(title=_("Questionnaire"), feedback_form=feedback_form),
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

    def has_played_before(self, session: Session) -> bool:
        """Check if the current participant has completed this game previously.

        Args:
            session: current session

        Returns:
            boolean indicating whether the current participant has finished a session of this game
        """
        previous_games = Session.objects.filter(
            participant=session.participant,
            block=session.block,
            finished_at__isnull=False,
        )
        if previous_games.count():
            return True
        return False

    def calculate_intermediate_score(self, session: Session, result: Result) -> int:
        """process result data during a trial (i.e., between next_round calls). This is only used in the matching_pairs rules files so far.
        Override this in your rules file to control what value should be returned when frontend calls `session/intermediate_score` endpoint.

        Args:
            session: current session
            result: result to be evaluated

        Returns:
            the score of the result
        """
        return 0

    def finalize(self, session: Session):
        """Mark the session as finished and calculate final scores"""
        session.finish(session.final_score)
        session.save_json_data(
            {
                "scores": self.get_score_data(session),
                **self.get_final_statistics(session),
            },
        )

    def get_final_statistics(self, session: Session) -> dict:
        return {}

    def get_score_data(self, session: Session) -> dict:
        return {
            "percentile": {
                "value": session.percentile_rank({"finished_at__isnull": False}),
                "label": "%",
            },
            "total": {
                "value": session.total_score(),
                "label": session.block.final.score_label or _("points"),
            },
            "accumulative": {
                "value": session.participant.accumulative_score(),
                "label": session.block.final.score_label or _("points"),
            },
        }

    def get_final_view(self, session: Session) -> dict:
        self.finalize(session)
        return session.block.final.convert_to_view(session)

    def validate_playlist(self, playlist: Playlist = None) -> list[str]:
        """Validate a playlist associated with this rules file, e.g., ensure that files have a specific name format

        Args:
            playlist: playlist to be checked

        Returns:
            an array of error messages. If return value is an empty list, validation succeeded.
        """
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
