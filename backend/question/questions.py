from django.conf import settings
from django.utils import translation

from experiment.actions.question import QuestionAction
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
from question.models import (
    QuestionGroup,
    Question,
    Choice,
    QuestionInSeries,
    QuestionSeries,
)
from question.profile_scoring_rules import PROFILE_SCORING_RULES

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


def create_default_questions():
    """Creates default questions and question groups in the database."""

    for group_key, questions in QUESTION_GROUPS_DEFAULT.items():

        if not QuestionGroup.objects.filter(key=group_key).exists():
            group = QuestionGroup.objects.create(key=group_key, editable=False)
        else:
            group = QuestionGroup.objects.get(key=group_key)

        for question in questions:
            q, created = Question.objects.get_or_create(key=question.key)

            # Create translatable fields
            for lang in settings.MODELTRANSLATION_LANGUAGES:
                lang_field = lang.replace("-", "_")
                translation.activate(lang)
                if hasattr(q, "question_" + lang_field):
                    setattr(q, "question_" + lang_field, str(question.text))
                    setattr(q, "explainer_" + lang_field, str(question.explainer))

            # Create other fields
            q.view = question.view
            q.editable = False
            for key in ['min_value', 'max_value', 'max_length', 'min_values']:
                set_question_attribute(question, q, key)

            q.save()

            if hasattr(question, 'choices'):
                keys = (
                    question.choices.keys()
                    if hasattr(question.choices, 'keys')
                    else range(0, len(question.choices))
                )
                index = 0
                for key in keys:
                    choice, _created = Choice.objects.get_or_create(
                        key=key,
                        question=q,
                    )
                    choice.text = str(question.choices[key])
                    choice.index = index
                    for lang in settings.MODELTRANSLATION_LANGUAGES:
                        lang_field = lang.replace("-", "_")
                        translation.activate(lang)
                        if hasattr(choice, "text_" + lang_field):
                            setattr(
                                choice, "text_" + lang_field, str(question.choices[key])
                            )
                    choice.save()
                    index += 1
            translation.activate("en")
            if created:
                group.questions.add(q)


def set_question_attribute(
    question_action: QuestionAction, question_object: Question, key: str
):
    try:
        attribute = getattr(question_action, key)
        if attribute:
            setattr(question_object, key, attribute)
    except AttributeError:
        pass
