from typing import Generator

from django.db.models import QuerySet

from experiment.actions.question import ChoiceQuestionAction, OpenQuestionAction
from participant.models import Participant
from question.models import Question
from result.utils import prepare_profile_result


def question_by_key(key: str, questions: list):
    """Return a copy of question with given key

    Args:
        key (str): Key of question

    Returns:
        the question, if it exists
    """
    return next((question for question in questions if question.key == key), None)


def adjust_question_choices(choices: dict, drop_keys: list[str]) -> dict:
    return {key: choices[key] for key in choices.keys() if key not in drop_keys}


def get_unanswered_questions(
    participant: Participant, question_set: QuerySet
) -> Generator:
    """Return next unasked profile question and prepare its result

    Args:
        participant (Participant): participant who will be checked for unanswered questions
        questions (list[Questions]): list of questions from which to select an unanswered question
        randomize (bool): optionally, randomize order of questions
        cutoff_index (int): Maximal index in a questions sequence to consider questions

    Yields:
        Next unasked profile question

    """
    keys_answered = participant.profile().values_list('question_key', flat=True)
    for question_obj in question_set:
        if question_obj.key in keys_answered:
            continue
        profile_result = prepare_profile_result(question_obj.key, participant)
        question = create_question_db(question_obj)
        question.result_id = profile_result.id
        yield question


def create_question_db(question: Question):
    """Creates experiment.actions.form.question object from a Question in the database with key

    Args:
        key: Key of Question

    Retuns:
        experiment.actions.form.Question object
    """
    if question.choice_set.count():
        choices = {}
        for choice in question.choice_set.all():
            choices[choice.key] = choice.text
        return ChoiceQuestionAction(
            key=question.key,
            text=question.question,
            explainer=question.explainer,
            choices=choices,
            view=question.view,
            min_values=question.min_values,
        )
    else:
        return OpenQuestionAction(
            key=question.key,
            text=question.question,
            explainer=question.explainer,
            min_value=question.min_value,
            max_value=question.max_value,
            max_length=question.max_length,
            view=question.view,
        )
