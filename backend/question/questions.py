from .demographics import DEMOGRAPHICS, EXTRA_DEMOGRAPHICS, DEMOGRAPHICS_OTHER
from .goldsmiths import MSI_F1_ACTIVE_ENGAGEMENT, MSI_F2_PERCEPTUAL_ABILITIES, MSI_F3_MUSICAL_TRAINING, MSI_F4_SINGING_ABILITIES, MSI_F5_EMOTIONS, MSI_OTHER, MSI_FG_GENERAL, MSI_ALL
from .languages import LANGUAGE, LANGUAGE_OTHER
from .musicgens import MUSICGENS_17_W_VARIANTS
from .stomp import STOMP
from .tipi import TIPI
from .other import OTHER
import random
from .models import QuestionGroup, Question

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

    return [QUESTIONS[key] for key in keys_all]


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

