from django.utils.translation import gettext_lazy as _

from experiment.rules.views.form import ChoiceQuestion, Question
from .iso_countries import ISO_COUNTRIES

# List of all available profile questions
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
        choices={
            'none': _("Have not (yet) completed any school qualification"),
            'isced-2': _("Vocational qualification at about 16 years of age (GCSE)"),
            'isced-3-4': _("Secondary diploma (A-levels/high school)"),
            'isced-5': _("Associate's degree or 2-year professional diploma"),
            'isced-6': _("Bachelor's degree or equivalent"),
            'isced-7': _("Master's degree or equivalent"),
            'isced-8': _("Doctoral degree or equivalent")
        }
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
        key='dgf_highest_qualification_expectation',
        view='RADIOS',
        question=_(
            "If you are still in education, what is the highest qualification you expect to obtain?"),
        choices={
            'none': _("First school qualification (A-levels/ High school"),
            'isced-2': _("Post-16 vocational course"),
            'isced-3-4': _("Second school qualification (A-levels/high school)"),
            'isced-5': _("Undergraduate degree or professional qualification"),
            'isced-6': _("Postgraduate degree"),
            'isced-7': _("Not applicable"),
        }
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
    )
]


def question_by_key(key, questions=DEMOGRAPHICS, is_skippable=None):
    """Return question by given key"""
    try:
        for question in questions:
            if question.key == key:
                # Set is_skippable
                if is_skippable is not None:
                    question.is_skippable = is_skippable

                return question

    except KeyError as error:
        print('KeyError: %s' % str(error))
        return None

    return None


def unasked_question(participant, questions=DEMOGRAPHICS, is_skippable=None, skip=0):
    """Get unasked question, optionally skip results"""
    try:
        profile_questions = participant.profile_questions()
        for question in questions:
            if not question['question']['key'] in profile_questions:
                if skip == 0:
                    # Set is_skippable
                    if is_skippable is not None:
                        question['question']['is_skippable'] = is_skippable

                    return question
                skip = skip - 1
    except KeyError as error:
        print('KeyError: %s' % str(error))
        return None

    return None


def next_question(session, questions=DEMOGRAPHICS, is_skippable=None, skip=0):
    """Get next question for given session, optionally skip questions to allow for multiple questions in a round"""

    # First: Ask all questions once
    question = unasked_question(
        participant=session.participant,
        questions=questions,
        is_skippable=is_skippable,
        skip=skip
    )
    if question:
        return question

    # Second: Suggest questions with empty answer at random
    profile = session.participant.random_empty_profile_question()
    if profile:
        return question_by_key(
            key=profile.question,
            questions=questions,
            is_skippable=is_skippable
        )

    # Finally: return None if all questions have been completed
    return None
