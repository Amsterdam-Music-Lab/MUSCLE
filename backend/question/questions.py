from io import text_encoding
from .demographics import DEMOGRAPHICS, EXTRA_DEMOGRAPHICS, DEMOGRAPHICS_OTHER
from .goldsmiths import MSI_F1_ACTIVE_ENGAGEMENT, MSI_F2_PERCEPTUAL_ABILITIES, MSI_F3_MUSICAL_TRAINING, MSI_F4_SINGING_ABILITIES, MSI_F5_EMOTIONS, MSI_OTHER, MSI_FG_GENERAL, MSI_ALL
from .languages import LANGUAGE, LANGUAGE_OTHER
from .musicgens import MUSICGENS_17_W_VARIANTS
from .stomp import STOMP
from .tipi import TIPI
from .other import OTHER
import random
from .models import QuestionGroup, Question, Choice
from experiment.actions.form import BooleanQuestion, ChoiceQuestion, LikertQuestion, LikertQuestionIcon, NumberQuestion, TextQuestion, AutoCompleteQuestion#, #RangeQuestion
from django.conf import settings
from django.utils import translation
import sys
from question.profile_scoring_rules import PROFILE_SCORING_RULES

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

    return [create_question_db(key) for key in keys_all]


def create_default_questions(overwrite = False):
    """Creates default questions and question groups in the database"""

    sys.stdout.write("Creating default questions...")
    for group_key, questions in QUESTION_GROUPS_DEFAULT.items():

        if not QuestionGroup.objects.filter(key = group_key).exists():
            group = QuestionGroup.objects.create(key = group_key, editable = False)
        else:
            group = QuestionGroup.objects.get(key = group_key)

        for question in questions:

            if overwrite:
                Question.objects.filter(key = question.key).delete()

            if not Question.objects.filter(key = question.key).exists():
                q = Question.objects.create(key = question.key, question = question.question, editable = False)

                # Create translatable fields
                cur_lang = translation.get_language()
                for lang in settings.MODELTRANSLATION_LANGUAGES:
                    translation.activate(lang)
                    q.question = str(question.question)
                    q.explainer = str(question.explainer)
                q.save()
                translation.activate(cur_lang)

                if hasattr(question,'choices'):
                    keys = question.choices.keys() if hasattr(question.choices,'keys') else range(0, len(question.choices))
                    index = 0
                    for key in keys:
                        choice = Choice(key=key, text=str(question.choices[key]), index=index, question=q)
                        for lang in settings.MODELTRANSLATION_LANGUAGES:
                            translation.activate(lang)
                            choice.text = str(question.choices[key])
                        translation.activate(cur_lang)
                        choice.save()
                        index += 1

                # Create non-translatable fields
                q.type = question.__class__.__name__
                if q.type == "ChoiceQuestion":
                    q.min_values = question.min_values
                    q.view = question.view
                    q.profile_scoring_rule = PROFILE_SCORING_RULES.get(q.key,'')
                elif q.type == "NumberQuestion":
                    q.min_value = question.min_value
                    q.max_value = question.max_value
                elif q.type == "TextQuestion":
                    q.max_length = question.max_length
                elif q.type == "LikertQuestion":
                    q.scale_steps = question.scale_steps
                    q.profile_scoring_rule = PROFILE_SCORING_RULES.get(q.key,'')
                elif q.type == "RadiosQuestion":
                    q.type = "ChoiceQuestion"
                    q.view = question.view # 'RADIOS'
                    q.profile_scoring_rule = PROFILE_SCORING_RULES.get(q.key,'')
                if q.type == "Question": # Only key='contact'
                    q.type = "TextQuestion"
                    q.is_skippable = True
                q.save()

            else:
                q = Question.objects.get(key = question.key)
            group.questions.add(q)
    print("Done")

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
