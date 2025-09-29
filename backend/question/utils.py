from typing import Generator

from django.db.models import Model, QuerySet

from question.models import ChoiceSet, Question
from question.choice_sets import get_choice_set, predefined_choice_sets
from question.choice_sets.education import adjust_question_choices
from question.catalogues import get_catalogue, predefined_catalogues


def catalogue_keys(catalogue_key: str) -> list[str]:
    '''return all keys from a predefined catalogue of questions'''
    catalogue = get_catalogue(catalogue_key)
    return [question.key for question in catalogue]


def create_choice_set(choice_set_key: str, choices: dict) -> ChoiceSet:
    '''given a `ChoiceQuestionAction`, make sure that its ChoiceSet and Choices are created or updated'''
    choice_set_obj, _created = ChoiceSet.objects.get_or_create(key=choice_set_key)
    choice_set_obj.create_choices(choices)
    return choice_set_obj


def create_education_variant(question_key: str, drop_keys: list[str]) -> Question:
    """create a variant of the `dgf_education` question with the given `question_key`, minus the choices defined by `drop_keys`"""
    edu_choices = adjust_question_choices(
        get_choice_set('ISCED_EDUCATION_LEVELS_FULL'), drop_keys
    )
    new_choiceset = create_choice_set(f'{question_key}_choices', edu_choices)
    return Question(
        key=question_key,
        question=Question.objects.get(key='dgf_education').question,
        type="RadiosQuestion",
        choices=new_choiceset,
    )


def create_questions_in_database(catalogue: list[Question]):
    """Given a Question initialized in a rules file, create objects in the database"""
    Question.objects.bulk_create(
        [question for question in catalogue], ignore_conflicts=True
    )


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
    keys_answered = participant.profile().values_list('question_key', flat=True)
    for question_obj in question_set:
        if question_obj.key in keys_answered:
            continue
        yield question_obj


def import_choice_sets():
    """Import all choice sets defined in `question.choice_sets` into the database"""
    for key in predefined_choice_sets.keys():
        choice_set_obj, _created = ChoiceSet.objects.get_or_create(key=key, locked=True)
        choice_set_obj.create_choices(predefined_choice_sets[key])


def import_questions(QuestionModel=Question):
    """Import all questions defined in `question.catalogues` into the database
    Since the ChoiceSets having been created is a prerequesite, this also happens here
    """
    import_choice_sets()
    for catalogue in predefined_catalogues.values():
        for question in catalogue:
            if getattr(question, 'choices'):
                actual_choice_set = ChoiceSet.objects.get(key=question.choices.key)
                question.choices = actual_choice_set
            question.editable = False
            # question.populate_translated_fields('question')
            # question.populate_translated_fields('explainer')
        QuestionModel.objects.bulk_create(
            [question for question in catalogue], ignore_conflicts=True
        )
