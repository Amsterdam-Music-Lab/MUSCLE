import logging
import math

logger = logging.getLogger(__name__)

def check_expected_response(result):
    if not result:
        return None
    try:
        return result.expected_response
    except Exception as e:
        logger.log(e)
        return None

def correctness_score(form_element, result):
    expected_response = check_expected_response(result)
    if expected_response and expected_response == form_element['value']:
        return 1
    else:
        return 0

def likert_score(form_element, result=None):
    return form_element['value']

def reverse_likert_score(form_element, result=None):
    return form_element['scale_steps'] + 1 - form_element['value']

def reaction_time_score(form_element, result, data):
    expected_response = check_expected_response(result)
    if expected_response:
        time = data.get('decision_time')
        if expected_response == form_element['value']:
            return math.ceil(cls.timeout - time)
        else:
            return math.floor(-time)

SCORING_RULES = {
    'CORRECTNESS': correctness_score,
    'LIKERT': likert_score,
    'REVERSE_LIKERT': reverse_likert_score,
    'REACTION_TIME': reaction_time_score
}