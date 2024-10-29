import logging
import math

from django.db.models import Q

logger = logging.getLogger(__name__)


def check_expected_response(result):
    try:
        return result.expected_response
    except Exception as e:
        logger.log(e)
        return None


def correctness_score(result, data):
    expected_response = check_expected_response(result)
    if expected_response and expected_response == result.given_response:
        return 1
    else:
        return 0


def boolean_score(result, data):
    if result.given_response == 'yes':
        return 1
    else:
        return 0


def likert_score(result, data):
    return int(data['value'])


def reverse_likert_score(result, data):
    return int(data['scale_steps']) + 1 - int(data['value'])


def categories_likert_score(result, data):
    choices = list(data['choices'].keys())
    return choices.index(data['value']) + 1


def reaction_time_score(result, data):
    expected_response = check_expected_response(result)
    json_data = result.json_data
    if expected_response and json_data:
        time = json_data.get('decision_time')
        timeout = json_data.get('config').get('response_time')
        if expected_response == data['value']:
            return math.ceil(timeout - time)
        else:
            return math.floor(-time)


def song_sync_recognition_score(result, data):
    if result.given_response == 'TIMEOUT' or result.given_response == 'no':
        return 0
    json_data = result.json_data
    if json_data:
        time = json_data.get('decision_time')
        timeout = json_data.get('config').get('response_time')
        return math.ceil(timeout - time)


def song_sync_continuation_score(result, data):
    ''' modify previous result and return None'''
    previous_result = result.session.last_result(["recognize"])
    if check_expected_response(result) != result.given_response:
        previous_result.score *= -1
        previous_result.save()
    return None


SCORING_RULES = {
    'BOOLEAN': boolean_score,
    'CORRECTNESS': correctness_score,
    'LIKERT': likert_score,
    'REVERSE_LIKERT': reverse_likert_score,
    'REACTION_TIME': reaction_time_score,
    'SONG_SYNC_RECOGNITION': song_sync_recognition_score,
    'SONG_SYNC_CONTINUATION': song_sync_continuation_score,
    'CATEGORIES_TO_LIKERT': categories_likert_score,
}
