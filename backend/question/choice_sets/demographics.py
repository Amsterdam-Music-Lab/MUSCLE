from django.utils.translation import gettext_lazy as _

from question.choice_sets.isced_education import ISCED_EDUCATION_LEVELS

GENDER_COMPLETE ={
    'male': _("Man"),
    'trans_male': _("Transgender man"),
    'trans_female': _("Transgender woman"),
    'female': _("Woman"),
    'non_conforming': _("Non-conforming or questioning"),
    'intersex': _("Intersex or two-spirit"),
    'non_answer': _("Prefer not to answer"),
}

GENDER_REDUCED = {
    'M': _("Male"),
    'F': _("Female"), 
    'X': _("Other"),
    'U': _("Undisclosed")
}

GENERATION = {
    'silent': _('1945 or earlier'),
    'boomer': _('1946–1964'),
    'gen_x': _('1965-1980'),
    'millenial': _('1981–1996'),
    'gen_z': _('1997 or later'),
}

MUSIC_GENRE ={
    'mellow': _("Dance/Electronic/New Age"),
    'unpretentious': _("Pop/Country/Religious"),
    'sophisticated': _("Jazz/Folk/Classical"),
    'intense': _("Rock/Punk/Metal"),
    'contemporary': _("Hip-hop/R&B/Funk"),
}

MUSICAL_EXPERIENCE = {
    'none': _("None"),
    'moderate': _("Moderate"),
    'extensive': _("Extensive"),
    'professional': _("Professional"),
}

OCCUPATIONAL_STATUS ={
    'student': _("Still at School"),
    'higher education': _("At University"),
    'full-time': _("In Full-time employment"),
    'part-time': _("In Part-time employment"),
    'flexible work': _("Self-employed"),
    'family': _("Homemaker/full time parent"),
    'unemployment': _("Unemployed"),
    'retirement': _("Retired"),
}

ATTAINED_EDUCATION = dict(
    ISCED_EDUCATION_LEVELS,
    **{'none':  _('Have not (yet) completed any school qualification')}
)

EXPECTED_EDUCATION = dict(
    ISCED_EDUCATION_LEVELS,
    **{'none': _('Not applicable')}
)