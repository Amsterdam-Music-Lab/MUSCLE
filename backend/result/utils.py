from typing import Any, Optional, Union

from participant.models import Participant
from question.models import Question
from result.score import SCORING_RULES
from session.models import Session

from .models import Result
from .score import ScoringData, LikertData, ChoiceData


def get_result(
    session: Session, data: Union[ScoringData, LikertData, ChoiceData]
) -> Result:
    """Retrieve and return a `Result` object for the given session
    Fall back to retrieve a profile result tied to `session.participant`

    Args:
        session: the `Session` object for which to retrieve the result
        data: a dictionary with `result_id`, `value` and optional other keys

    Returns:
        a `Result` object

    Raises:
        Result.DoesNotExist: if there is no `result_id` in the data, or a result with that id does not exist
    """
    result_id = data.get("result_id")
    try:
        result = Result.objects.get(pk=result_id, session=session)
    except Result.DoesNotExist:
        # check if a profile type result exists
        try:
            result = Result.objects.get(pk=result_id, participant=session.participant)
        except Result.DoesNotExist:
            raise
    return result


def handle_results(data: dict, session: Session):
    """
    Given the data from the frontend, go through the `form` array and retrieve and score results

    Args:
        data: the data passed from the frontend
        session: the session for which results should be defined

    Raises:
        KeyError: if the request data does not contain a `form`
    """
    try:
        form = data.pop("form")
    except KeyError:
        raise KeyError('No `form` found in request data')
    for form_element in form:
        result = get_result(session, form_element)
        # save relevant data such as config and decision time (except for the popped form)
        result.save_json_data(data)
        result.save()
        result = score_result(
            form_element, session
        )  # TODO: raise Exceptions from underlying score functions


def prepare_profile_result(
    question_key: str,
    participant: Participant,
    **kwargs: Any,
) -> Result:
    """Get or create a profile `Result` object (i.e., tied to a `Participant` instead of a `Session`)
    As profile Results are usually demographic questions, they are not tied to a `section` or an `expected_response`

    Args:
        question_key: the key of the question in the questionnaire dictionaries
        participant: the participant on which the Result is going to be registered
        **kwargs: can be any other field(s) defined on the `Result` model

    Returns:
        `Result` object
    """
    scoring_rule = Question.objects.get(key=question_key).profile_scoring_rule
    result, created = Result.objects.get_or_create(
        question_key=question_key,
        participant=participant,
        scoring_rule=scoring_rule,
        **kwargs,
    )
    return result


def prepare_result(
    question_key: str,
    session: Session,
    **kwargs: Any,
) -> int:
    """Create a `Result` object, and provide its id to be serialized

    Args:
        question_key: the key of the question in the questionnaire dictionaries
        session: the session on which the Result is going to be registered
        **kwargs: can be any other field(s) defined on the `Result` model

    Returns:
        the id of the created `Result` object

    Raises:
        ValueError: in case an undefined `scoring_rule` keyword argument is provided
    """
    if kwargs.get('scoring_rule'):
        scoring_rule = kwargs.get('scoring_rule')
        if not SCORING_RULES.get(scoring_rule):
            raise ValueError(
                f"Scoring rule {scoring_rule} is not defined. Admissible values: {SCORING_RULES.keys()}"
            )

    result = Result.objects.create(
        question_key=question_key,
        session=session,
        **kwargs,
    )
    return result.id


def score_result(
    data: Union[ScoringData, LikertData, ChoiceData], session: Session
) -> Result:
    """
    Retrieve the result for the given session, based on the frontend's `form` data,
    and populate the `json_data`, `given_response`, and `score` fields

    Args:
        session: a Session object
        data: a dictionary with `result_id`, `value` and optional other keys

    Returns:
        the retrieved and modified `Result` object
    """
    result = get_result(session, data)
    result.save_json_data(data)
    result.given_response = data.get("value")
    # Calculate score: by default, apply a scoring rule
    # Can be overridden by defining calculate_score in the rules file
    if result.session:
        score = session.block_rules().calculate_score(result, data)
        # refresh session data in case anything was changed within calculate_score function
        session.refresh_from_db()
    else:
        # this is a profile type result, i.e., it doesn't have a session:
        score = apply_scoring_rule(result, data)
    # Populate and save the result
    # result can also be None
    result.score = score
    result.save()
    return result


def apply_scoring_rule(
    result: Result, data: Union[ScoringData, LikertData, ChoiceData]
) -> Optional[float]:
    """Given a `Result` object and the `data`, apply the `scoring_rule` registered on the result

    Args:
        result: the `Result` object
        data: a dictionary with `result_id`, `value` and optional other keys

    Returns:
        the value of the score (integer or float), `None` if the `scoring_rule` is not defined
    """
    scoring_rule = SCORING_RULES.get(result.scoring_rule)
    if scoring_rule:
        return scoring_rule(result, data)
    return None
