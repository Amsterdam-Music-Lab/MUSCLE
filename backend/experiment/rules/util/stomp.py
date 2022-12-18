from experiment.rules.views.form import LikertQuestion

def stomp_question(key, genre):
    """Define a standard STOMP question for a genre"""
    return LikertQuestion(
        key = key,
        question = "How much do you like %s music?" % genre,
        choices = [
            "Dislike Strongly",
            "Dislike Moderately",
            "Dislike a Little",
            "Neither Like nor Dislike",
            "Like a Little",
            "Like Moderately",
            "Like Strongly"
        ],
        explainer = "Indicate your musical preferences"
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
