import logging
import math
from typing import TypedDict, Union

from result.models import Result

logger = logging.getLogger(__name__)


class ScoringData(TypedDict):
    value: Union[int, str]


class LikertData(ScoringData):
    scale_steps: int


class ChoiceData(ScoringData):
    choices: dict

def correctness_score(result: Result, data: ScoringData) -> int:
    """Binary score: return 1 if the participant's response is equal to the expected response, 0 otherwise"""
    if (
        result.expected_response == result.given_response
    ):  # TODO: raise exception if expected_response or given_response are `None`
        return 1
    else:
        return 0


def boolean_score(result: Result, data: ScoringData) -> int:
    """Binary score: return 1 if participant answered `yes`, 0 otherwise"""
    if result.given_response == 'yes':
        return 1
    else:
        return 0


def likert_score(result: Result, data: LikertData) -> int:
    """Translate the `n`th category of a Likert scale into `n`"""
    return int(data['value'])


def reverse_likert_score(result: Result, data: LikertData) -> int:
    """Translate the `n`th category of a Likert scale into `n_steps - n`"""
    return int(data['scale_steps']) + 1 - int(data['value'])


def categories_likert_score(result: Result, data: ChoiceData) -> int:
    """Translate the `n`th category of a dictionary of choices into `n`"""
    choices = list(data['choices'].keys())
    return choices.index(data['value']) + 1


def reaction_time_score(result: Result, data: ScoringData) -> float:
    """Return the difference between the configured maximal `response_time`
    and the participant's reaction time (`decision_time`)
    If the answer of the participant is incorrect, return the negative reaction time
    """
    expected_response = result.expected_response
    json_data = (
        result.json_data
    )  # TODO: raise exception if either expected_response or json_data is `None`
    if expected_response and json_data:
        time = json_data.get(
            'decision_time'
        )  # TODO: raise exception if json_data does not contain decision_time
        timeout = json_data.get('config').get(
            'response_time'
        )  # TODO: raise exception if json_data does not contain config with response_time
        if expected_response == data['value']:
            return math.ceil(timeout - time)
        else:
            return math.floor(-time)


def song_sync_recognition_score(result: Result, data: ScoringData) -> float:
    """First step of SongSync scoring (used in experiment.rules.hooked and derivatives):
    if the participant gives no (timeout) or a negative response to 'Do you know this song?', return 0
    otherwise, return the decision time
    """
    if result.given_response == 'TIMEOUT' or result.given_response == 'no':
        return 0
    json_data = result.json_data
    if json_data:
        time = json_data.get(
            'decision_time'
        )  # TODO: raise exception if time or timeout are `None`
        timeout = json_data.get('config').get('response_time')
        return math.ceil(timeout - time)


def song_sync_continuation_score(result: Result, data: dict):
    """Second step of the SongSync scoring, only happens if recognition score was nonzero.
    After continuation of audio, participants need to decide whether it was continued in the correct place.
    If answered incorrectly, this function modifies the reaction time score of the previous step.
    """
    previous_result = result.session.last_result(["recognize"])
    if result.expected_response != result.given_response:
        previous_result.score *= (
            -1
        )  # will raise exception if `previous_result.score = None`
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
