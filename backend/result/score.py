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


class ScoringError(Exception):
    """Custom exception when scoring fails"""

    pass


def correctness_score(result: Result, data: ScoringData) -> int:
    """Binary score: return 1 if the participant's response is equal to the expected response, 0 otherwise

    Args:
        result: the result to be scored
        data: the participant's response
    """
    if result.expected_response == None:
        raise ScoringError(
            "`expected_response` not defined but needed for `correctness_score`"
        )
    if result.expected_response == result.given_response:
        return 1
    else:
        return 0


def boolean_score(result: Result, data: ScoringData) -> int:
    """Binary score: return 1 if participant answered `yes`, 0 otherwise

    Args:
        result: the result to be scored
        data: the participant's response
    """
    if result.given_response == 'yes':
        return 1
    else:
        return 0


def _score_likert(data: LikertData) -> tuple[list[str], int]:
    """Return the choices of the Likert question as a list, return index of selected value in that list"""
    choices = [choice.get('value') for choice in data.get('choices')]
    return choices, choices.index(str(data.get('value')))


def likert_score(result: Result, data: LikertData) -> int:
    """Translate the `n`th category of a Likert scale into `n`

    Args:
        result: the result to be scored
        data: the participant's response
    """
    _choices, score = _score_likert(data)
    return score + 1


def reverse_likert_score(result: Result, data: LikertData) -> int:
    """Translate the `n`th category of a Likert scale into `n_steps - n`

    Args:
        result: the result to be scored
        data: the participant's response
    """
    choices, score = _score_likert(data)
    return len(choices) - score


def reaction_time_score(result: Result, data: ScoringData) -> float:
    """Return the difference between the configured maximal `response_time`
    and the participant's reaction time (`decision_time`)

    If the answer of the participant is incorrect, return the negative reaction time

    Args:
        result: the result to be scored
        data: the participant's response
    """
    expected_response = result.expected_response
    if expected_response == None:
        raise ScoringError(
            "`expected_response` not defined but needed for `reaction_time_score`"
        )
    json_data = result.json_data
    if json_data == None:
        raise ScoringError(
            "No `json_data` defined but needed for `reaction_time_score`"
        )
    if expected_response and json_data:
        time = json_data.get('decision_time')
        if time == None:
            raise ScoringError(
                "No `decision_time` sent from frontend, but needed for `reaction_time_score`"
            )
        timeout = json_data.get('response_time')
        if timeout == None:
            raise ScoringError(
                "No `response_time` defined, but needed for `reaction_time_score`"
            )
        if expected_response == data['value']:
            return math.ceil(timeout - time)
        else:
            return math.floor(-time)


def song_sync_recognition_score(result: Result, data: ScoringData) -> float:
    """First step of SongSync scoring (used in experiment.rules.hooked and derivatives):

    If the participant gives no response or negative response to 'Do you know this song?', return 0
    otherwise, return the decision time

    Args:
        result: the result to be scored
        data: the participant's response
    """
    if result.given_response == 'TIMEOUT' or result.given_response == 'no':
        return 0
    json_data = result.json_data
    if json_data:
        time = json_data.get('decision_time')
        if time == None:
            raise ScoringError(
                "No `decision_time` sent from the frontend but needed for `song_sync_recognition_score`"
            )
        timeout = json_data.get('response_time')
        if timeout == None:
            raise ValueError(
                "No `response_time` defined, but needed for `song_sync_recognition_score`"
            )
        return math.ceil(timeout - time)


def song_sync_verification_score(result: Result, data: ScoringData):
    """Second step of the SongSync scoring, only happens if participant stated they know the song,
    used to verify that the statement was truthful.

    After continuation of audio, participants need to decide whether it was continued in the correct place.
    If answered incorrectly, this function modifies the reaction time score of the previous step.

    Args:
        result: the result to be scored
        data: the participant's response
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
    'SONG_SYNC_VERIFICATION': song_sync_verification_score,
}
