import logging

logger = logging.getLogger(__name__)


def correctness_score(form_element, session_id):
    result = get_result(session_id, form_element['result_id'])
    if not result:
        return None
    try:
        expected_response = result.expected_response
    except Exception as e:
        logger.log(e)
        expected_response = None
    if expected_response and expected_response == form_element['value']:
        return 1
    else:
        return 0

def likert_score(form_element, session_id):
    return form_element['value']

def reverse_likert_score(form_element, session_id):
    return form_element['scale_steps'] + 1 - form_element['value']

def reaction_time_score(form_element, session_id):
    pass

def get_result(session_id=None, result_id=None):
    from experiment.models import Result, Session
    try:
        session = Session.objects.get(pk=session_id)
    except Session.DoesNotExist:
        return None

    if result_id:
        try:
            result = Result.objects.get(pk=result_id, session=session)
        except Result.DoesNotExist:
            # Create new result
            result = Result(session=session)
    else:
        result = Result(session=session)
    return result

SCORING_RULES = {
    'CORRECTNESS': correctness_score,
    'LIKERT': likert_score,
    'REVERSE_LIKERT': reverse_likert_score,
    'REACTION_TIME': reaction_time_score
}