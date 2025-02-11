from copy import deepcopy
import random

from result.utils import prepare_profile_result


def copy_shuffle(questions):
    """ Makes a shuffled copy of a sequence of questions.

    Args:
    questions: A sequence of questions

    Returns:
    A shuffled copy of questions
    """
    qcopy = deepcopy(questions)
    random.shuffle(qcopy)
    return qcopy


def total_unanswered_questions(participant, questions):
    """ Return how many questions have not been answered yet by the participant

    Args:
        participant: Participant who answer questions
        questions: Sequence of questions

    Returns:
        Number of unanswered questions
    """
    profile_questions = participant.profile().values_list('question_key', flat=True)
    return len([question for question in questions if question.key not in profile_questions])


def question_by_key(key, questions, is_skippable=None, drop_choices=[]):
    """Return a copy of question with given key

    Args:
        key: Key of question
        questions: Sequence of questions
        is_skippable: True will make the returned questions skippable
        drop_choices: Choices in the question to be removed (if applicable)

    Returns:
        A copy of question
    """
    for question in questions:
        if question.key == key:
            q = deepcopy(question)
            # Question is_skippable
            if is_skippable is not None:
                q.is_skippable = is_skippable
            if hasattr(question, 'choices') and len(drop_choices):
                for choice in drop_choices:
                    q.choices.pop(choice, None)
            return q
    return None


def unanswered_questions(participant, questions, randomize=False, cutoff_index=None):
    """Generator to give next unasked profile question and prepare its result

    Args:
        participant: participant who will be checked for unanswered questions
        questions: list of questions from which to select an unanswered question
        randomize: optionally, randomize order of questions
        cutoff_index: Maximal index in a questions sequence to consider questions

    Yields:
        Next unasked profile question

    """
    if randomize:
        random.shuffle(questions)
    for question in questions[:cutoff_index]:
        profile_result = prepare_profile_result(question.key, participant)
        if profile_result.given_response is None:
            q = deepcopy(question)
            q.result_id = profile_result.pk
            yield q
