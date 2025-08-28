from django.utils.translation import gettext_lazy as _

from experiment.actions.question import TextRangeQuestion, RadiosQuestion


def musicgens_question(key: str, text: str) -> TextRangeQuestion:
    """Define a standard MusicGens question"""
    return TextRangeQuestion(
        key=key,
        text=text,
        choices={
            1: _("Never"),
            2: _("Rarely"),
            3: _("Once in a while"),
            4: _("Sometimes"),
            5: _("Very often"),
            6: _("Always"),
        },
        explainer=_("Please tell us how much you agree"),
        scoring_rule='LIKERT',
    )


def musicgens_radio_question(key: str, text: str) -> RadiosQuestion:
    """Define a MusicGens question with three radio buttons """
    return RadiosQuestion(
        key=key, text=text, choices={1: _("Yes"), 0: _("No"), -1: _("I'm not sure")}
    )


MUSICGENS_17_W_VARIANTS = [
    musicgens_question(
        "P01_1",
        _("Can you clap in time with a musical beat?")
    ),
    musicgens_question(
        "P01_2",
        _("I can tap my foot in time with the beat of the music I hear.")
    ),
    musicgens_question(
        "P01_3",
        _("When listening to music, can you move in time with the beat?")
    ),
    musicgens_question(
        "P02_1",
        _("I can recognise a piece of music after hearing just a few notes.")
    ),
    musicgens_question(
        "P02_2",
        _("I can easily recognise a familiar song.")
    ),
    musicgens_question(
        "P02_3",
        _("When I hear the beginning of a song I know immediately whether I've heard it before or not.")
    ),
    musicgens_question(
        "P03_1",
        _("I can tell when people sing out of tune.")
    ),
    musicgens_question(
        "P03_2",
        _("I am able to judge whether someone is a good singer or not.")
    ),
    musicgens_question(
        "P03_3",
        _("I find it difficult to spot mistakes in a performance of a song even if I know the tune.")
    ),
    musicgens_question(
        "P04_1",
        _("I feel chills when I hear music that I like.")
    ),
    musicgens_question(
        "P04_2",
        _("I get emotional listening to certain pieces of music.")
    ),
    musicgens_question(
        "P04_3",
        _("I become tearful or cry when I listen to a melody that I like very much.")
    ),
    musicgens_question(
        "P04_4",
        _("Music gives me shivers or goosebumps.")
    ),
    musicgens_question(
        "P05_1",
        _("When I listen to music I'm absorbed by it.")
    ),
    musicgens_question(
        "P05_2",
        _("While listening to music, I become so involved that I forget about myself and my surroundings.")
    ),
    musicgens_question(
        "P05_3",
        _("When I listen to music I get so caught up in it that I don't notice anything.")
    ),
    musicgens_question(
        "P05_4",
        _("I feel like I am 'one' with the music.")
    ),
    musicgens_question(
        "P05_5",
        _("I lose myself in music.")
    ),
    musicgens_question(
        "P06_1",
        _("I like listening to music.")
    ),
    musicgens_question(
        "P06_2",
        _("I enjoy music.")
    ),
    musicgens_question(
        "P06_3",
        _("I listen to music for pleasure.")
    ),
    musicgens_question(
        "P06_4",
        _("Music is kind of an addiction for me - I couldn't live without it.")
    ),
    musicgens_question(
        "P07_1",
        _("I can tell when people sing or play out of time with the beat of the music.")
    ),
    musicgens_question(
        "P07_2",
        _("I can hear when people are not in sync when they play a song.")
    ),
    musicgens_question(
        "P07_3",
        _("I can tell when music is sung or played in time with the beat.")
    ),
    musicgens_question(
        "P08_1",
        _("I can sing or play a song from memory.")
    ),
    musicgens_question(
        "P08_2",
        _("Singing or playing music from memory is easy for me.")
    ),
    musicgens_question(
        "P08_3",
        _("I find it hard to sing or play a song from memory.")
    ),
    musicgens_question(
        "P09_1",
        _("When I sing, I have no idea whether I'm in tune or not.")
    ),
    musicgens_question(
        "P09_2",
        _("I am able to hit the right notes when I sing along with a recording.")
    ),
    musicgens_question(
        "P09_3",
        _("I can sing along with other people.")
    ),
    musicgens_question(
        "P10_1",
        _("I have no sense for rhythm (when I listen, play or dance to music).")
    ),
    musicgens_question(
        "P10_2",
        _("Understanding the rhythm of a piece is easy for me (when I listen, play or dance to music).")
    ),
    musicgens_question(
        "P10_3",
        _("I have a good sense of rhythm (when I listen, play, or dance to music).")
    ),
    musicgens_radio_question(
        "P11_1",
        _("Do you have absolute pitch? Absolute pitch is the ability to recognise and name an isolated musical tone without a reference tone, e.g. being able to say 'F#' if someone plays that note on the piano."),
    ),
    musicgens_radio_question(
        "P11_2",
        _("Do you have perfect pitch?"),
    ),
    musicgens_radio_question(
        "P11_3",
        _("If someone plays a note on an instrument and you can't see what note it is, can you still name it (e.g. say that is a 'C' or an 'F')?")
    ),
    musicgens_question(
        "P12_1",
        _("Can you hear the difference between two melodies?")
    ),
    musicgens_question(
        "P12_2",
        _("I can recognise differences between melodies even if they are similar.")
    ),
    musicgens_question(
        "P12_3",
        _("I can tell when two melodies are the same or different.")
    ),
    musicgens_question(
        "P13_1",
        _("I make up new melodies in my mind.")
    ),
    musicgens_question(
        "P13_2",
        _("I make up songs, even when I'm just singing to myself.")
    ),
    musicgens_question(
        "P13_3",
        _("I like to play around with new melodies that come to my mind.")
    ),
    musicgens_question(
        "P14_1",
        _("I have a melody stuck in my mind.")
    ),
    musicgens_question(
        "P14_2",
        _("I experience earworms.")
    ),
    musicgens_question(
        "P14_3",
        _("I get music stuck in my head.")
    ),
    musicgens_question(
        "P14_4",
        _("I have a piece of music stuck on repeat in my head.")
    ),
    musicgens_question(
        "P15_1",
        _("Music makes me dance.")
    ),
    musicgens_question(
        "P15_2",
        _("I don't like to dance, not even with music I like.")
    ),
    musicgens_question(
        "P15_3",
        _("I can dance to a beat.")
    ),
    musicgens_question(
        "P15_4",
        _("I easily get into a groove when listening to music.")
    ),
    musicgens_question(
        "P16_1",
        _("Can you hear the difference between two rhythms?")
    ),
    musicgens_question(
        "P16_2",
        _("I can tell when two rhythms are the same or different.")
    ),
    musicgens_question(
        "P16_3",
        _("I can recognise differences between rhythms even if they are similar.")
    ),
    musicgens_question(
        "P17_1",
        _("I can't help humming or singing along to music that I like.")
    ),
    musicgens_question(
        "P17_2",
        _("When I hear a tune I like a lot I can't help tapping or moving to its beat.")
    ),
    musicgens_question(
        "P17_3",
        _("Hearing good music makes me want to sing along.")
    )
]

MUSICGENS_EXTRA = [
    RadiosQuestion(
        key="PHENOTYPES_1",
        text=_(
            "Please select the sentence that describes your level of achievement in music."
        ),
        choices={
            1: _("I have no training or recognised talent in this area."),
            2: _("I play one or more musical instruments proficiently."),
            3: _("I have played with a recognised orchestra or band."),
            4: _("I have composed an original piece of music."),
            5: _("My musical talent has been critiqued in a local publication."),
            6: _("My composition has been recorded."),
            7: _("Recordings of my composition have been sold publicly."),
            8: _("My compositions have been critiqued in a national publication."),
            9: _(
                " My compositions have been critiqued in multiple national publications."
            ),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_2",
        text=_(
            "How engaged with music are you? Singing, playing, and even writing music counts here. Please choose the answer which describes you best."
        ),
        choices={
            1: _("I am not engaged in music at all."),
            2: _(
                "I am self-taught and play music privately, but I have never played, sung, or shown my music to others."
            ),
            3: _(
                "I have taken lessons in music, but I have never played, sung, or shown my music to others."
            ),
            4: _(
                "I have played or sung, or my music has been played in public concerts in my home town, but I have not been paid for this."
            ),
            5: _(
                "I have played or sung, or my music has been played in public concerts in my home town, and I have been paid for this."
            ),
            6: _("I am professionally active as a musician."),
            7: _(
                "I am professionally active as a musician and have been reviewed/featured in the national or international media and/or have received an award for my musical activities."
            ),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_3",
        text=_("I have never been complimented for my talents as a musical performer."),
        choices={
            1: _("Completely disagree"),
            2: _("Strongly disagree"),
            3: _("Disagree"),
            4: _("Neither agree nor disagree"),
            5: _("Agree"),
            6: _("Strongly agree"),
            7: _("Completely agree"),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_4",
        text=_(
            "To what extent do you agree that you see yourself as someone who is sophisticated in art, music, or literature?"
        ),
        choices={
            1: _("Agree strongly"),
            2: _("Agree moderately"),
            3: _("Agree slightly"),
            4: _("Disagree slightly"),
            5: _("Disagree moderately"),
            6: _("Disagree strongly"),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_5",
        text=_(
            "At the peak of my interest, I practised ___ hours on my primary instrument (including voice)."
        ),
        choices={
            1: _("0"),
            2: _("0.5"),
            3: _("1"),
            4: _("1.5"),
            5: _("3–4"),
            6: _("5 or more"),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_6",
        text=_("How often did you play or sing during the most active period?"),
        choices={
            1: _("Every day"),
            2: _("More than 1x per week"),
            3: _("1x per week"),
            4: _("1x per month"),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_7",
        text=_(
            "How long (duration) did you play or sing during the most active period?"
        ),
        choices={
            1: _("More than 1 hour per week"),
            2: _("1 hour per week"),
            3: _("Less than 1 hour per week"),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_8",
        text=_(
            "About how many hours do you usually spend each week playing a musical instrument?"
        ),
        choices={
            1: _("None"),
            2: _("1 hour or less a week"),
            3: _("2–3 hours a week"),
            4: _("4–5 hours a week"),
            5: _("6–7 hours a week"),
            6: _("8 or more hours a week"),
        },
    ),
    RadiosQuestion(
        key="PHENOTYPES_9",
        text=_(
            "Indicate approximately how many hours per week you have played or practiced any musical instrument at all, i.e., all different instruments, on average over the last 10 years."
        ),
        choices={
            1: _("less than 1 hour per week"),
            2: _("1 hour per week"),
            3: _("2 hours per week"),
            4: _("3 hours per week"),
            5: _("4–5 hours per week"),
            6: _("6–9 hours per week"),
            7: _("10–14 hours per week"),
            8: _("15–24 hours per week"),
            9: _("25–40 hours per week"),
            10: _("41 or more hours per week"),
        },
    ),
]
