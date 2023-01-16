from copy import deepcopy

from django.utils.translation import gettext_lazy as _

from experiment.actions.form import ChoiceQuestion, Question
from .iso_countries import ISO_COUNTRIES
from .iso_languages import ISO_LANGUAGES
from .isced_education import ISCED_EDUCATION_LEVELS
from experiment.util.profile_scoring_rules import PROFILE_SCORING_RULES

from result.utils import prepare_result

# List of all available profile questions

ATTAINED_EDUCATION_CHOICES = dict(
    ISCED_EDUCATION_LEVELS,
    **{'none':  _('Have not (yet) completed any school qualification')}
)
EXPECTED_EDUCATION_CHOICES = dict(
    ISCED_EDUCATION_LEVELS,
    **{'none': _('Not applicable')}
)

DEMOGRAPHICS = [
    ChoiceQuestion(
        key='dgf_gender_identity',
        view='RADIOS',
        question=_("With which gender do you currently most identify?"),
        choices={
            'male': _("Man"),
            'trans_male': _("Transgender man"),
            'trans_female': _("Transgender woman"),
            'female': _("Woman"),
            'non_conforming': _("Non-conforming or questioning"),
            'intersex': _("Intersex or two-spirit"),
            'non_answer': _("Prefer not to answer")
        }
    ),
    ChoiceQuestion(
        key='dgf_generation',
        view='RADIOS',
        question=_("When were you born?"),
        choices={
            'silent': _('1943 or earlier'),
            'boomer': _('1946–1964'),
            'gen_x': _('1965-1980'),
            'millenial': _('1981–1996'),
            'gen_z': _('1997 or later')
        }
    ),
    ChoiceQuestion(
        key='dgf_country_of_origin',
        view='DROPDOWN',
        question=_(
            "In which country did you spend the most formative years of your childhood and youth?"),
        choices=ISO_COUNTRIES
    ),
    ChoiceQuestion(
        key='dgf_education',
        view='RADIOS',
        question=_(
            "What is the highest educational qualification that you have attained?"),
        choices=ATTAINED_EDUCATION_CHOICES
    ),
    ChoiceQuestion(
        key='dgf_country_of_residence',
        view='DROPDOWN',
        question=_("In which country do you currently reside?"),
        choices=ISO_COUNTRIES
    ),
    ChoiceQuestion(
        key='dgf_genre_preference',
        view='RADIOS',
        question=_(
            "To which group of musical genres do you currently listen most?"),
        choices={
            'mellow': _("Dance/Electronic/New Age"),
            'unpretentious': _("Pop/Country/Religious"),
            'sophisticated': _("Jazz/Folk/Classical"),
            'intense': _("Rock/Punk/Metal"),
            'contemporary': _("Hip-hop/R&B/Funk")
        }
    ),
    Question(
        key='msi_39_best_instrument',
        view='STRING',
        question=_("The instrument I play best, including voice (or none), is:")
    ),
]


EXTRA_DEMOGRAPHICS = [
    Question(
        key='dgf_age',
        view='STRING',
        question=_("What is your age?")
    ),
    Question(
        key='dgf_country_of_origin_open',
        view='STRING',
        question=_(
            "In which country did you spend the most formative years of your childhood and youth?"),
    ),
    Question(
        key='dgf_country_of_residence_open',
        view='STRING',
        question=_("In which country do you currently reside?")
    ),
    ChoiceQuestion(
        key='dgf_native_language',
        view='DROPDOWN',
        question="What is your native language?",
        choices=ISO_LANGUAGES
    ),
    ChoiceQuestion(
        key='dgf_highest_qualification_expectation',
        view='RADIOS',
        question=_(
            "If you are still in education, what is the highest qualification you expect to obtain?"),
        choices=EXPECTED_EDUCATION_CHOICES
    ),
    ChoiceQuestion(
        key='dgf_occupational_status',
        view='RADIOS',
        question=_("Occupational status"),
        choices={
            'student': _("Still at School"),
            'higher education': _("At University"),
            'full-time': _("In Full-time employment"),
            'part-time': _("In Part-time employment"),
            'flexible work': _("Self-employed"),
            'family': _("Homemaker/full time parent"),
            'unemployment': _("Unemployed"),
            'retirement': _("Retired")
        }
    ),
    ChoiceQuestion(
        key='dgf_gender_reduced',
        view='RADIOS',
        question=_("What is your gender?"),
        choices={
            'M': "Male",
            'F': "Female",
            'X': "Other",
            'U': "Undisclosed"
        }
    ),
]


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


def unasked_question(session, questions=DEMOGRAPHICS, is_skippable=False):
    """Get unasked question, optionally skip results"""
    profile_questions = session.participant.profile_questions()
    for question in questions:
        if not question.key in profile_questions:
            q = deepcopy(question)
            # Question is_skippable
            if is_skippable != None:
                q.is_skippable = is_skippable
            return q
    return None

def next_question(session, questions=DEMOGRAPHICS, continue_with_random=False, is_skippable=False):
    """Get next question of a list of questions for given session
    - questions: list of questions to be asked
    - is_skippable: set to True if a given question can be skipped
    - continue_with_random: set to True if the function should return
    random non-asked questions after initial list has been answered
    """
    # First: Ask all questions once
    question = unasked_question(
        session=session,
        questions=questions,
        is_skippable=is_skippable
    )
    if question:
        question.result_id = prepare_result(
            session,
            is_profile=True,
            scoring_rule=PROFILE_SCORING_RULES.get(question.key, '')
        )
        return question

    if continue_with_random:
    # Optionally, suggest questions with empty answer at random
        empty_result = session.participant.random_empty_profile_question()
        if empty_result:
            return question_by_key(
                key=empty_result.question_key,
                questions=questions,
                is_skippable=is_skippable
            )

    # Finally: return None if all questions have been completed
    return None
