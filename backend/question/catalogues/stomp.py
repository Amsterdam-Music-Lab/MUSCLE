from django.utils.translation import gettext_lazy as _

from experiment.actions.question import TextRangeQuestion


def stomp_question(key: str, genre: str) -> TextRangeQuestion:
    """Define a standard STOMP question for a genre"""
    return TextRangeQuestion(
        key=key,
        text=_("How much do you like %s music?") % genre,
        choices={
            1: _("Dislike Strongly"),
            2: _("Dislike Moderately"),
            3: _("Dislike a Little"),
            4: _("Neither Like nor Dislike"),
            5: _("Like a Little"),
            6: _("Like Moderately"),
            7: _("Like Strongly"),
        },
        explainer="Indicate your musical preferences",
        scoring_rule='LIKERT',
    )


STOMP20 = [
    stomp_question('stomp_alternative', 'alternative'),
    stomp_question('stomp_blues', 'blues'),
    stomp_question('stomp_classical', 'classical'),
    stomp_question('stomp_country', 'country'),
    stomp_question('stomp_dance', 'dance and electronic'),
    stomp_question('stomp_folk', 'folk'),
    stomp_question('stomp_funk', 'funk'),
    stomp_question('stomp_gospel', 'gospel'),
    stomp_question('stomp_metal', 'heavy metal'),
    stomp_question('stomp_world', 'world'),
    stomp_question('stomp_jazz', 'jazz'),
    stomp_question('stomp_new_age', 'new-age'),
    stomp_question('stomp_opera', 'opera'),
    stomp_question('stomp_pop', 'pop'),
    stomp_question('stomp_punk', 'punk'),
    stomp_question('stomp_rap', 'rap and hip-hop'),
    stomp_question('stomp_reggae', 'reggae'),
    stomp_question('stomp_religious', 'religious'),
    stomp_question('stomp_rock', 'rock'),
    stomp_question('stomp_rnb', 'soul and R&B'),
]

STOMP = STOMP20 + [
    stomp_question('stomp_bluegrass', 'bluegrass'), # Almost unknown in Europe
    stomp_question('stomp_oldies', 'oldies'), # not used in MUSIC scoring
    stomp_question('stomp_soundtracks', 'soundtracks and theme-song'), # not used in MUSIC scoring
]
