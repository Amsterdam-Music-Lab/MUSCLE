from django.utils.translation import gettext_lazy as _

from experiment.actions.question import (
    DropdownQuestion,
    NumberQuestion,
    RadiosQuestion,
    TextQuestion,
)
from question.choice_sets.isced_education import ISCED_EDUCATION_LEVELS
from question.choice_sets.iso_countries import ISO_COUNTRIES
from question.choice_sets.iso_languages import ISO_LANGUAGES
from question.utils import question_by_key


ATTAINED_EDUCATION_CHOICES = dict(
    ISCED_EDUCATION_LEVELS,
    **{'none':  _('Have not (yet) completed any school qualification')}
)
EXPECTED_EDUCATION_CHOICES = dict(
    ISCED_EDUCATION_LEVELS,
    **{'none': _('Not applicable')}
)

DEMOGRAPHICS = [
    RadiosQuestion(
        key='dgf_gender_identity',
        text=_("With which gender do you currently most identify?"),
        choices={
            'male': _("Man"),
            'trans_male': _("Transgender man"),
            'trans_female': _("Transgender woman"),
            'female': _("Woman"),
            'non_conforming': _("Non-conforming or questioning"),
            'intersex': _("Intersex or two-spirit"),
            'non_answer': _("Prefer not to answer"),
        },
    ),
    RadiosQuestion(
        key='dgf_generation',
        text=_("When were you born?"),
        choices={
            'silent': _('1945 or earlier'),
            'boomer': _('1946–1964'),
            'gen_x': _('1965-1980'),
            'millenial': _('1981–1996'),
            'gen_z': _('1997 or later'),
        },
    ),
    DropdownQuestion(
        key='dgf_country_of_origin',
        text=_(
            "In which country did you spend the most formative years of your childhood and youth?"
        ),
        choices=ISO_COUNTRIES,
    ),
    RadiosQuestion(
        key='dgf_education',
        text=_("What is the highest educational qualification that you have attained?"),
        choices=ATTAINED_EDUCATION_CHOICES,
    ),
    DropdownQuestion(
        key='dgf_country_of_residence',
        text=_("In which country do you currently reside?"),
        choices=ISO_COUNTRIES,
    ),
    RadiosQuestion(
        key='dgf_genre_preference',
        text=_("To which group of musical genres do you currently listen most?"),
        choices={
            'mellow': _("Dance/Electronic/New Age"),
            'unpretentious': _("Pop/Country/Religious"),
            'sophisticated': _("Jazz/Folk/Classical"),
            'intense': _("Rock/Punk/Metal"),
            'contemporary': _("Hip-hop/R&B/Funk"),
        },
    ),
]


EXTRA_DEMOGRAPHICS = [
    NumberQuestion(key='dgf_age', text=_("What is your age?")),
    TextQuestion(
        key='dgf_country_of_origin_open',
        text=_(
            "In which country did you spend the most formative years of your childhood and youth?"
        ),
    ),
    TextQuestion(
        key='dgf_country_of_residence_open',
        text=_("In which country do you currently reside?"),
    ),
    DropdownQuestion(
        key='dgf_native_language',
        text="What is your native language?",
        choices=ISO_LANGUAGES,
    ),
    RadiosQuestion(
        key='dgf_highest_qualification_expectation',
        text=_(
            "If you are still in education, what is the highest qualification you expect to obtain?"
        ),
        choices=EXPECTED_EDUCATION_CHOICES,
    ),
    RadiosQuestion(
        key='dgf_occupational_status',
        text=_("Occupational status"),
        choices={
            'student': _("Still at School"),
            'higher education': _("At University"),
            'full-time': _("In Full-time employment"),
            'part-time': _("In Part-time employment"),
            'flexible work': _("Self-employed"),
            'family': _("Homemaker/full time parent"),
            'unemployment': _("Unemployed"),
            'retirement': _("Retired"),
        },
    ),
    RadiosQuestion(
        key='dgf_gender_reduced',
        text=_("What is your gender?"),
        choices={'M': "Male", 'F': "Female", 'X': "Other", 'U': "Undisclosed"},
    ),
    RadiosQuestion(
        key='dgf_musical_experience',
        text=_("Please select your level of musical experience:"),
        choices={
            'none': _("None"),
            'moderate': _("Moderate"),
            'extensive': _("Extensive"),
            'professional': _("Professional"),
        },
    ),
]


def demographics_other():
    questions = []
    question = create_education_variant(
        'dgf_education_matching_pairs', ['isced-2', 'isced-5']
    )
    questions.append(question)
    question = create_education_variant(
        'dgf_education_gold_msi', drop_choices=['isced-1']
    )
    questions.append(question)
    question = create_education_variant('dgf_education_huang_2022', ['isced-5'])
    questions.append(question)
    return questions


def create_education_variant(question_key, drop_choices):
    education_question = question_by_key('dgf_education', DEMOGRAPHICS)
    education_choices = ISCED_EDUCATION_LEVELS
    question = RadiosQuestion(
        text=education_question.text,
        key=question_key,
        choices={
            key: value
            for key, value in education_choices.items()
            if key not in drop_choices
        },
    )
    return question


DEMOGRAPHICS_OTHER = demographics_other() + [
    TextQuestion(
        key='fame_name', text=_("Enter a name to enter the ICMPC hall of fame")
    )
]
