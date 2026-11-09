import random
from re import compile, sub

from django.utils.translation import gettext_lazy as _

def camelize(input_str: str) -> str:
    """convert a snake_case to camelCase string"""
    snake_case_pattern = compile(r'_([a-z])')
    return sub(snake_case_pattern, lambda match: match.group(1).upper(), input_str)


def randomize_playhead(min_jitter, max_jitter, continuation_correctness) -> float:
    """
    Description: Randomly add to the playhead offset. If `continuation_correctness=True`, this function returns 0, and has no effect on the playhead.

    Args:
        min_jitter (float): Minimum offset.
        max_jitter (float): Maximum offset.
        continuation_correctness (bool): whether to add a random increment to the continued audio

    Returns:
        (float): The random offset.
    """

    return random.uniform(min_jitter, max_jitter) if not continuation_correctness else 0
