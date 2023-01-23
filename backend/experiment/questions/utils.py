from copy import deepcopy
import random

from .profile_scoring_rules import PROFILE_SCORING_RULES
from .demographics import DEMOGRAPHICS

from result.utils import prepare_result
from result.models import Result

# List of all available profile questions



def total_unanswered_questions(session, questions=DEMOGRAPHICS):
    """ Return how many questions have not been answered yet by the participant"""
    profile_questions = session.participant.profile().exclude(
        given_response=None
    ).values_list('question_key', flat=True)
    return len(list(set(profile_questions).difference(set([
        question.key for question in questions
    ]))))

def question_by_key(key, questions=DEMOGRAPHICS, is_skippable=None, drop_choices=[]):
    """Return question by given key"""
    for question in questions:
        if question.key == key:
            q = deepcopy(question)
            # Question is_skippable
            if is_skippable != None:
                q.is_skippable = is_skippable
            if hasattr(question, 'choices') and len(drop_choices):
                for choice in drop_choices:
                    q.choices.pop(choice, None)
            return q
    return None

def unasked_question(session, questions=DEMOGRAPHICS, randomize=False, is_skippable=False):
    """Get unasked question
    - session: session whose participant will be checked for unanswerd questions
    - questions: list of questions from which to select an unanswered question
    - optionally, randomize order of questions
    - optionally, make question skipabble
    """
    if randomize:
        random.shuffle(questions)
    profile_questions = session.participant.profile_questions()
    for question in questions:
        if not question.key in profile_questions:
            q = deepcopy(question)
            # Question is_skippable
            if is_skippable != None:
                q.is_skippable = is_skippable
            try:
                result_id = session.participant.profile().get(question_key=q.key)
            except Result.DoesNotExist:
                result_id = prepare_result(
                    session,
                    is_profile=True,
                    scoring_rule=PROFILE_SCORING_RULES.get(question.key, '')
                )
            q.result_id = result_id
            return q
    return None
