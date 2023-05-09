from experiment.actions.form import LikertQuestion, RadiosQuestion

def musicgens_question(key, question):
    """Define a standard MusicGens question"""
    return LikertQuestion(
        key = key,
        question = question,
        choices = {
            1: "Never",
            2: "Not Very Often",
            3: "Occasionally",
            4: "Sometimes",
            5: "Very Often",
            6: "Always"
        },
        explainer = "Please tell us how much you agree"
    )

MUSICGENS_17_W_VARIANTS = [
    musicgens_question(
        "P01_1",
        "Can you clap in time with a musical beat?"
    ),
    musicgens_question(
        "P01_2",
        "I can tap my foot in time with the beat of the music I hear."
    ),
    musicgens_question(
        "P01_3",
        "When listening to music, can you move in time with the beat?"
    ),
    musicgens_question(
        "P02_1",
        "I can recognise a piece of music after hearing just a few notes."
    ),
    musicgens_question(
        "P02_2",
        "I can easily recognise a familiar song."
    ),
    musicgens_question(
        "P02_3",
        "When I hear the beginning of a song I know immediately whether I've heard it before or not."
    ),
    musicgens_question(
        "P03_1",
        "I can tell when people sing out of tune."
    ),
    musicgens_question(
        "P03_2",
        "I am able to judge whether someone is a good singer or not."
    ),
    musicgens_question(
        "P03_3",
        "I find it difficult to spot mistakes in a performance of a song even if I know the tune."
    ),
    musicgens_question(
        "P04_1",
        "I feel chills when I hear music that I like."
    ),
    musicgens_question(
        "P04_2",
        "I get emotional listening to certain pieces of music."
    ),
    musicgens_question(
        "P04_3",
        "I become tearful or cry when I listen to a melody that I like very much."
    ),
    musicgens_question(
        "P04_4",
        "Music gives me shivers or goosebumps."
    ),
    musicgens_question(
        "P05_1",
        "When I listen to music I'm absorbed by it."
    ),
    musicgens_question(
        "P05_2",
        "While listening to music, I become so involved that I forget about myself and my surroundings."
    ),
    musicgens_question(
        "P05_3",
        "When I listen to music I get so caught up in it that I don't notice anything."
    ),
    musicgens_question(
        "P05_4",
        "I feel like I am 'one' with the music."
    ),
    musicgens_question(
        "P05_5",
        "I lose myself in music."
    ),
    musicgens_question(
        "P06_1",
        "I like listening to music."
    ),
    musicgens_question(
        "P06_2",
        "I enjoy music."
    ),
    musicgens_question(
        "P06_3",
        "I listen to music for pleasure."
    ),
    musicgens_question(
        "P06_4",
        "Music is kind of an addiction for me - I couldn't live without it."
    ),
    musicgens_question(
        "P07_1",
        "I can tell when people sing or play out of time with the beat of the music."
    ),
    musicgens_question(
        "P07_2",
        "I can hear when people are not in sync when they play a song."
    ),
    musicgens_question(
        "P07_3",
        "I can tell when music is sung or played in time with the beat."
    ),
    musicgens_question(
        "P08_1",
        "I can sing or play a song from memory."
    ),
    musicgens_question(
        "P08_2",
        "Singing or playing music from memory is easy for me."
    ),
    musicgens_question(
        "P08_3",
        "I find it hard to sing or play a song from memory."
    ),
    musicgens_question(
        "P09_1",
        "When I sing, I have no idea whether I'm in tune or not."
    ),
    musicgens_question(
        "P09_2",
        "I am able to hit the right notes when I sing along with a recording."
    ),
    musicgens_question(
        "P09_3",
        "I can sing along with other people."
    ),
    musicgens_question(
        "P10_1",
        "I have no sense for rhythm (when I listen, play or dance to music)."
    ),
    musicgens_question(
        "P10_2",
        "Understanding the rhythm of a piece is easy for me (when I listen, play or dance to music)."
    ),
    musicgens_question(
        "P10_3",
        "I have a good sense of rhythm (when I listen, play, or dance to music)."
    ),
    RadiosQuestion(
        key = "P11_1",
        question = "Do you have absolute pitch? Absolute pitch is the ability to recognise and name an isolated musical tone without a reference tone, e.g. being able to say 'F#' if someone plays that note on the piano.",
        choices = {
            1: "Yes",
            0: "No",
            -1: "I'm Not Sure"
        }
    ),
    RadiosQuestion(
        key="P11_2",
        question="Do you have perfect pitch?",
        choices = {
            1: "Yes",
            0: "No",
            -1: "I'm Not Sure"
        }
    ),
    RadiosQuestion(
        key="P11_3",
        question="If someone plays a note on an instrument and you can't see what note it is, can you still name it (e.g. say that is a 'C' or an 'F')?",
        choices = {
            1: "Yes",
            0: "No",
            -1: "I'm Not Sure"
        }
    ),
    musicgens_question(
        "P12_1",
        "Can you hear the difference between two melodies?"
    ),
    musicgens_question(
        "P12_2",
        "I can recognise differences between melodies even if they are similar."
    ),
    musicgens_question(
        "P12_3",
        "I can tell when two melodies are the same or different."
    ),
    musicgens_question(
        "P13_1",
        "I make up new melodies in my mind."
    ),
    musicgens_question(
        "P13_2",
        "I make up songs, even when I'm just singing to myself."
    ),
    musicgens_question(
        "P13_3",
        "I like to play around with new melodies that come to my mind."
    ),
    musicgens_question(
        "P14_1",
        "I have a melody stuck in my mind."
    ),
    musicgens_question(
        "P14_2",
        "I experience earworms."
    ),
    musicgens_question(
        "P14_3",
        "I get music stuck in my head."
    ),
    musicgens_question(
        "P14_4",
        "I have a piece of music stuck on repeat in my head."
    ),
    musicgens_question(
        "P15_1",
        "Music makes me dance."
    ),
    musicgens_question(
        "P15_2",
        "I don't like to dance, not even with music I like."
    ),
    musicgens_question(
        "P15_3",
        "I can dance to a beat."
    ),
    musicgens_question(
        "P15_4",
        "I easily get into a groove when listening to music."
    ),
    musicgens_question(
        "P16_1",
        "Can you hear the difference between two rhythms?"
    ),
    musicgens_question(
        "P16_2",
        "I can tell when two rhythms are the same or different."
    ),
    musicgens_question(
        "P16_3",
        "I can recognise differences between rhythms even if they are similar."
    ),
    musicgens_question(
        "P17_1",
        "I can't help humming or singing along to music that I like."
    ),
    musicgens_question(
        "P17_2",
        "When I hear a tune I like a lot I can't help tapping or moving to its beat."
    ),
    musicgens_question(
        "P17_3",
        "Hearing good music makes me want to sing along."
    )
]
