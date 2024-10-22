from session.models import Session
from .models import Result

from question.profile_scoring_rules import PROFILE_SCORING_RULES
from result.score import SCORING_RULES

from question.models import Question

def get_result(session, data):
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


def handle_results(data, session):
    """
    if the given_result is an array of results, retrieve and save results for all of them
    else, handle results at top level
    """
    form = data.pop("form")
    for form_element in form:
        result = get_result(session, form_element)
        # save relevant data such as config and decision time (except for the popped form)
        result.save_json_data(data)
        result.save()
        result = score_result(form_element, session)
    return result


def prepare_profile_result(question_key, participant, **kwargs):
    """Create a Result object, and provide its id to be serialized
    - question_key: the key of the question in the questionnaire dictionaries
    - participant: the participant on which the Result is going to be registered
    possible kwargs:
        - expected_response: optionally, provide the correct answer, used for scoring
        - comment: optionally, provide a comment to be saved in the database
        - scoring_rule: optionally, provide a scoring rule
    """
    scoring_rule = Question.objects.get(key=question_key).profile_scoring_rule
    result, created = Result.objects.get_or_create(
        question_key=question_key, participant=participant, scoring_rule=scoring_rule, **kwargs
    )
    return result


def prepare_result(question_key: str, session: Session, **kwargs) -> int:
    """Create a Result object, and provide its id to be serialized
    - question_key: the key of the question in the questionnaire dictionaries
    - session: the session on which the Result is going to be registered
    possible kwargs:
        - section: optionally, provide a section to which the Result is going to be tied
        - expected_response: optionally, provide the correct answer, used for scoring
        - json_data: optionally, provide json data tied to this result
        - comment: optionally, provide a comment to be saved in the database, e.g. "training phase"
        - scoring_rule: optionally, provide a scoring rule
    """
    result = Result.objects.create(question_key=question_key, session=session, **kwargs)
    return result.id


def score_result(data, session):
    """
    Create a result for given session, based on the result data
    (form element or top level data)
    parameters:
    session: a Session object
    data: a dictionary, containing a result_id, and optional other params:
    {
        result_id: int [optional]
        params: ...
    }
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


def apply_scoring_rule(result, data):
    scoring_rule = SCORING_RULES.get(result.scoring_rule)
    if scoring_rule:
        return scoring_rule(result, data)
    return None
