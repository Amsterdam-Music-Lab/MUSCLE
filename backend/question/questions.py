import random

from django.conf import settings
from django.utils import translation

from question.catalogues.demographics import (
    DEMOGRAPHICS,
    EXTRA_DEMOGRAPHICS,
    DEMOGRAPHICS_OTHER,
)
from question.catalogues.goldsmiths import (
    MSI_F1_ACTIVE_ENGAGEMENT,
    MSI_F2_PERCEPTUAL_ABILITIES,
    MSI_F3_MUSICAL_TRAINING,
    MSI_F4_SINGING_ABILITIES,
    MSI_F5_EMOTIONS,
    MSI_OTHER,
    MSI_FG_GENERAL,
    MSI_ALL,
)
from question.catalogues.languages import LANGUAGE, LANGUAGE_OTHER
from question.catalogues.musicgens import MUSICGENS_17_W_VARIANTS
from question.catalogues.stomp import STOMP
from question.catalogues.tipi import TIPI
from question.catalogues.other import OTHER
from question.catalogues.vanderbilt import (
    THATS_MY_SONG_QUESTIONS_FIXED,
    THATS_MY_SONG_QUESTIONS_RANDOM,
)
from question.models import QuestionGroup, Question, Choice
from question.profile_scoring_rules import PROFILE_SCORING_RULES
from question.utils import create_question_db

# Default QuestionGroups used by command createquestions
QUESTION_GROUPS_DEFAULT = {
    "DEMOGRAPHICS": DEMOGRAPHICS,
    "EXTRA_DEMOGRAPHICS": EXTRA_DEMOGRAPHICS,
    "MSI_F1_ACTIVE_ENGAGEMENT": MSI_F1_ACTIVE_ENGAGEMENT,
    "MSI_F2_PERCEPTUAL_ABILITIES": MSI_F2_PERCEPTUAL_ABILITIES,
    "MSI_F3_MUSICAL_TRAINING": MSI_F3_MUSICAL_TRAINING,
    "MSI_F4_SINGING_ABILITIES": MSI_F4_SINGING_ABILITIES,
    "MSI_F5_EMOTIONS": MSI_F5_EMOTIONS,
    "MSI_OTHER": MSI_OTHER,
    "MSI_FG_GENERAL": MSI_FG_GENERAL,
    "MSI_ALL": MSI_ALL,
    "LANGUAGE": LANGUAGE,
    "MUSICGENS_17_W_VARIANTS": MUSICGENS_17_W_VARIANTS,
    "STOMP": STOMP,
    "STOMP20": STOMP,
    "TIPI": TIPI,
    "OTHER": OTHER,
    "DEMOGRAPHICS_OTHER": DEMOGRAPHICS_OTHER,
    "LANGUAGE_OTHER": LANGUAGE_OTHER,
    "THATS_MY_SONG_FIXED": THATS_MY_SONG_QUESTIONS_FIXED,
    "THATS_MY_SONG_RANDOM": THATS_MY_SONG_QUESTIONS_RANDOM,
}

QUESTIONS = {}
QUESTION_GROUPS = {}

for group, questions in QUESTION_GROUPS_DEFAULT.items():
    for question in questions:
        QUESTIONS[question.key] = question
    QUESTION_GROUPS[group] = [ q.key for q in questions ]


def create_default_questions(question_model=Question, choice_model=Choice, question_group_model=QuestionGroup):
    """Creates default questions and question groups in the database. Can be used with historical models.

    Args:
        question_model: Question model
        choice_model: Choice model
        question_group_model: QuestionGroup model

    Returns:
        None
    """

    for group_key, questions in QUESTION_GROUPS_DEFAULT.items():

        if not question_group_model.objects.filter(key = group_key).exists():
            group = question_group_model.objects.create(key = group_key, editable = False)
        else:
            group = question_group_model.objects.get(key = group_key)

        for question in questions:

            if not question_model.objects.filter(key = question.key).exists():
                q = question_model.objects.create(
                    key=question.key, question=question.text, editable=False
                )

                # Create translatable fields
                for lang in settings.MODELTRANSLATION_LANGUAGES:
                    lang_field = lang.replace("-","_")
                    translation.activate(lang)

                    # This should work, but doesn't
                    # q.question = str(question.question)
                    # q.explainer = str(question.explainer)

                    if hasattr(q, "question_"+lang_field):
                        setattr(q, "question_" + lang_field, str(question.text))
                        setattr(q, "explainer_"+lang_field, str(question.explainer))

                q.save()

                if hasattr(question,'choices'):
                    keys = question.choices.keys() if hasattr(question.choices,'keys') else range(0, len(question.choices))
                    index = 0
                    for key in keys:
                        choice = choice_model(key=key, text=str(question.choices[key]), index=index, question=q)
                        for lang in settings.MODELTRANSLATION_LANGUAGES:
                            lang_field = lang.replace("-","_")
                            translation.activate(lang)
                            # choice.text = str(question.choices[key])
                            if hasattr(choice, "text_"+lang_field):
                                setattr(choice,"text_"+lang_field, str(question.choices[key]))
                        choice.save()
                        index += 1

                translation.activate("en")

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
                q = question_model.objects.get(key = question.key)
            group.questions.add(q)


def populate_translation_fields(lang, question_model=Question):
    """ Populates django-modeltraslation model fields from translations in .po files.

    Args:
        lang (str): Language code
        question_model: Question model. Can be used with historical models

    Returns:
        None
    """

    lang_field = lang.replace("-","_")

    translation.activate(lang)

    for group_key, questions in QUESTION_GROUPS_DEFAULT.items():
        for question in questions:

            q = question_model.objects.get(key = question.key)

            # This should work, but doesn't
            # q.question = str(question.question)
            # q.explainer = str(question.explainer)

            setattr(q, "question_" + lang_field, str(question.text))
            setattr(q, "explainer_"+lang_field, str(question.explainer))

            q.save()

            if hasattr(question,'choices'):
                keys = question.choices.keys() if hasattr(question.choices,'keys') else range(0, len(question.choices))
                for key in keys:
                    choice = q.choice_set.all().get(key=key)
                    # choice.text = str(question.choices[key])
                    setattr(choice,"text_"+lang_field, str(question.choices[key]))
                    choice.save()

    translation.activate('en')
