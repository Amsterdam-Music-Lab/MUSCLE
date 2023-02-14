from django.utils.translation import gettext_lazy as _

from experiment.actions.form import ChoiceQuestion, Question
from experiment.standards.iso_countries import ISO_COUNTRIES
from experiment.standards.iso_languages import ISO_LANGUAGES
from experiment.standards.isced_education import ISCED_EDUCATION_LEVELS

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
    ChoiceQuestion(
        key='dgf_musical_experience',
        view='RADIOS',
        question=_("Please select your level of musical experience:"),
        choices={
            'none': _("None"),
            'moderate': _("Moderate"),
            'extensive': _("Extensive"),
            'professional': _("Professional")
        }
    )
]
