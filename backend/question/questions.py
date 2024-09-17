from .demographics import DEMOGRAPHICS, EXTRA_DEMOGRAPHICS, DEMOGRAPHICS_OTHER
from .goldsmiths import MSI_F1_ACTIVE_ENGAGEMENT, MSI_F2_PERCEPTUAL_ABILITIES, MSI_F3_MUSICAL_TRAINING, MSI_F4_SINGING_ABILITIES, MSI_F5_EMOTIONS, MSI_OTHER, MSI_FG_GENERAL, MSI_ALL
from .languages import LANGUAGE, LANGUAGE_OTHER
from .musicgens import MUSICGENS_17_W_VARIANTS
from .stomp import STOMP
from .tipi import TIPI
from .other import OTHER
import random
from .models import QuestionGroup, Question
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, LikertQuestion, LikertQuestionIcon, NumberQuestion, TextQuestion, AutoCompleteQuestion#, #RangeQuestion

# Default QuestionGroups used by command createquestions
QUESTION_GROUPS_DEFAULT = { "DEMOGRAPHICS" : DEMOGRAPHICS,
    "EXTRA_DEMOGRAPHICS" : EXTRA_DEMOGRAPHICS,
    "MSI_F1_ACTIVE_ENGAGEMENT" : MSI_F1_ACTIVE_ENGAGEMENT,
    "MSI_F2_PERCEPTUAL_ABILITIES" : MSI_F2_PERCEPTUAL_ABILITIES,
    "MSI_F3_MUSICAL_TRAINING" : MSI_F3_MUSICAL_TRAINING,
    "MSI_F4_SINGING_ABILITIES" : MSI_F4_SINGING_ABILITIES,
    "MSI_F5_EMOTIONS" : MSI_F5_EMOTIONS,
    "MSI_OTHER" : MSI_OTHER,
    "MSI_FG_GENERAL" : MSI_FG_GENERAL,
    "MSI_ALL" : MSI_ALL,
    "LANGUAGE" : LANGUAGE,
    "MUSICGENS_17_W_VARIANTS" : MUSICGENS_17_W_VARIANTS,
    "STOMP" : STOMP,
    "STOMP20" : STOMP,
    "TIPI" : TIPI,
    "OTHER" : OTHER,
    "DEMOGRAPHICS_OTHER" : DEMOGRAPHICS_OTHER,
    "LANGUAGE_OTHER" : LANGUAGE_OTHER
}

QUESTIONS = {}
QUESTION_GROUPS = {}

for group, questions in QUESTION_GROUPS_DEFAULT.items():
    for question in questions:
        QUESTIONS[question.key] = question
    QUESTION_GROUPS[group] = [ q.key for q in questions ]


def get_questions_from_series(questionseries_set):

    keys_all = []

    for questionseries in questionseries_set:
        keys = [qis.question.key for qis in questionseries.questioninseries_set.all()]
        if questionseries.randomize:
            random.shuffle(keys)
        keys_all.extend(keys)

    return [QUESTIONS.get(key, create_question_db(key)) for key in keys_all]


def create_default_questions():
    """Creates default questions and question groups in the database"""

    for group_key, questions in QUESTION_GROUPS_DEFAULT.items():

        if not QuestionGroup.objects.filter(key = group_key).exists():
            group = QuestionGroup.objects.create(key = group_key, editable = False)
        else:
            group = QuestionGroup.objects.get(key = group_key)

        for question in questions:
            if not Question.objects.filter(key = question.key).exists():
                q = Question.objects.create(key = question.key, question = question.question, editable = False)
            else:
                q = Question.objects.get(key = question.key)
            group.questions.add(q)

def create_question_db(key):
    """ Creates form.question object from a Question in the database with key"""

    question = Question.objects.get(key=key)

    choices = {}
    for choice in question.choice_set.all():
        choices[choice.key] = choice.text

    if question.type == "LikertQuestion":
        return LikertQuestion(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            scale_steps = question.scale_steps,
            choices = choices
            )
    elif question.type == "LikertQuestionIcon":
        return LikertQuestionIcon(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            scale_steps = question.scale_steps
            )
    elif question.type == "NumberQuestion":
        return NumberQuestion(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            min_value = question.min_value,
            max_value = question.max_value
            )
    elif question.type == "TextQuestion":
        return TextQuestion(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            max_length=question.max_length
            )
    elif question.type == "BooleanQuestion":
        return BooleanQuestion(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            choices = choices
            )
    elif question.type == "ChoiceQuestion":
        return ChoiceQuestion(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            choices = choices,
            min_values=question.min_values,
            view=question.view
            )
    elif question.type == "AutoCompleteQuestion":
        return AutoCompleteQuestion(
            key=question.key,
            question=question.question,
            explainer = question.explainer,
            choices = choices
            )
