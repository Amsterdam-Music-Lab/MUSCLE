from typing import Generator

from django.db.models import Model, QuerySet


def get_unanswered_questions(participant: Model, question_set: QuerySet) -> Generator:
    """Return next unasked profile question and prepare its result

    Args:
        participant (Participant): participant who will be checked for unanswered questions
        questions (list[Questions]): list of questions from which to select an unanswered question
        randomize (bool): optionally, randomize order of questions
        cutoff_index (int): Maximal index in a questions sequence to consider questions

    Yields:
        Next unasked profile question

    """
    keys_answered = participant.profile_results().values_list('question_key', flat=True)
    for question_obj in question_set:
        if question_obj.key in keys_answered:
            continue
        yield question_obj
