from experiment.actions.form import LikertQuestion, RadiosQuestion

def musicgens_question(key, question):
    """Define a standard MusicGens question"""
    return LikertQuestion(
        key = key,
        question = question,
        choices = {
            1: "Never",
            2: "Rarely",
            3: "Once in a while",
            4: "Sometimes",
            5: "Very often",
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
            -1: "I'm not sure"
        }
    ),
    RadiosQuestion(
        key="P11_2",
        question="Do you have perfect pitch?",
        choices = {
            1: "Yes",
            0: "No",
            -1: "I'm not sure"
        }
    ),
    RadiosQuestion(
        key="P11_3",
        question="If someone plays a note on an instrument and you can't see what note it is, can you still name it (e.g. say that is a 'C' or an 'F')?",
        choices = {
            1: "Yes",
            0: "No",
            -1: "I'm not sure"
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

MUSICGENS_EXTRA = [
    RadiosQuestion(
        key = "PHENOTYPES_1",
        question = "Please select the sentence that describes your level of achievement in music.",
        choices = {
            1: "I have no training or recognised talent in this area.",
            2: "I play one or more musical instruments proficiently.",
            3: "I have played with a recognised orchestra or band.",
            4: "I have composed an original piece of music.",
            5: "My musical talent has been critiqued in a local publication.",
            6: "My composition has been recorded.",
            7: "Recordings of my composition have been sold publicly.",
            8: "My compositions have been critiqued in a national publication.",
            9: " My compositions have been critiqued in multiple national publications."
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_2",
        question = "How engaged with music are you? Singing, playing, and even writing music counts here. Please choose the answer which describes you best.",
        choices = {
            1: "I am not engaged in music at all.",
            2: "I am self-taught and play music privately, but I have never played, sung, or shown my music to others.",
            3: "I have taken lessons in music, but I have never played, sung, or shown my music to others.",
            4: "I have played or sung, or my music has been played in public concerts in my home town, but I have not been paid for this.",
            5: "I have played or sung, or my music has been played in public concerts in my home town, and I have been paid for this.",
            6: "I am professionally active as a musician.",
            7: "I am professionally active as a musiciean and have been reviewed/featured in the national or international media and/or have received an award for my musical activities."
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_3",
        question = "I have never been complimented for my talents as a musical performer.",
        choices = {
            1: "Completely disagree",
            2: "Strongly disagree",
            3: "Disagree",
            4: "Neither agree nor disagree",
            5: "Agree",
            6: "Strongly agree",
            7: "Completely agree"
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_4",
        question = "To what extent do you agree that you see yourself as someone who is sophisticated in art, music, or literature?",
        choices = {
            1: "Agree strongly",
            2: "Agree moderately",
            3: "Agree slightly",
            4: "Disagree slightly",
            5: "Disagree moderately",
            6: "Disagree strongly"
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_5",
        question = "At the peak of my interest, I practised ___ hours on my primary instrument (including voice).",
        choices = {
            1: "0",
            2: "0.5",
            3: "1",
            4: "1.5",
            5: "3–4",
            6: "5 or more"
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_6",
        question = "How often did you play or sing during the most active period?",
        choices = {
            1: "Every day",
            2: "More than 1x per week",
            3: "1x per week",
            4: "1x per month"
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_7",
        question = "How long (duration) did you play or sing during the most active period?",
        choices = {
            1: "More than 1 hour per week",
            2: "1 hour per week",
            3: "Less than 1 hour per week"
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_8",
        question = "About how many hours do you usually spend each week playing a musical instrument?",
        choices = {
            1: "None",
            2: "1 hour or less a week",
            3: "2–3 hours a week",
            4: "4–5 hours a week",
            5: "6–7 hours a week",
            6: "8 or more hours a week"
        }
    ),
    RadiosQuestion(
        key = "PHENOTYPES_9",
        question = "Indicate approximately how many hours per week you have played or practiced any musical instrument at all, i.e., all different instruments, on average over the last 10 years.",
        choices = {
            1: "less than 1 hour per week",
            2: "1 hour per week",
            3: "2 hours per week",
            4: "3 hours per week",
            5: "4–5 hours per week",
            6: "6–9 hours per week",
            7: "10–14 hours per week",
            8: "15–24 hours per week",
            9: "25–40 hours per week",
            10: "41 or more hours per week"
        }
    )
]
