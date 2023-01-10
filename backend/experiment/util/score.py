import logging
import math

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

def likert_score(result, data):
    return int(data['value'])

def reverse_likert_score(result, data):
    return int(data['scale_steps']) + 1 - int(data['value'])

def categories_likert_score(result, data):
    choices = list(data['choices'].keys())
    return choices.index(data['value']) + 1

def reaction_time_score(result, data):
    expected_response = check_expected_response(result)
    if expected_response:
        time = data.get('decision_time')
        timeout = data.get('config').get('decision_time')
        if expected_response == data['value']:
            return math.ceil(timeout - time)
        else:
            return math.floor(-time)

def song_sync_score(result, data):
    score = 0
    # Calculate from the data object
    # If requested keys don't exist, return None
    try:
        config = data['config']
        result = data['result']
        # Calculate scores based on result type
        if result['type'] == 'time_passed':
            score = 0
        elif result['type'] == 'not_recognized':
            score = 0
        elif result['type'] == 'recognized':
            # Get score
            score = math.ceil(
                config['recognition_time'] - result['recognition_time']
            )
            if config['continuation_correctness'] != result['continuation_correctness']:
                score *= -1
    except KeyError as error:
        logger.warning('KeyError: %s' % str(error))
        return None
    return score


SCORING_RULES = {
    'CORRECTNESS': correctness_score,
    'LIKERT': likert_score,
    'REVERSE_LIKERT': reverse_likert_score,
    'REACTION_TIME': reaction_time_score,
    'SONG_SYNC': song_sync_score,
    'CATEGORIES_TO_LIKERT': categories_likert_score,
}