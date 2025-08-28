from django.utils.translation import gettext_lazy as _

from experiment.actions.question import RadiosQuestion, TextQuestion, TextRangeQuestion
from question.utils import question_by_key
from question.choice_sets.general import LIKERT_AGREE_7
from question.choice_sets.goldsmiths import (
    GMSI_ATTENDED_EVENTS,
    GMSI_DAILY_MUSIC_LISTENING,
    GMSI_HOURS_DAILY_PRACTICE,
    GMSI_N_INSTRUMENTS,
    GMSI_YEARS_INSTRUMENTAL_TRAINING,
    GMSI_YEARS_PRACTICED,
    GMSI_YEARS_THEORY_TRAINING,
)


def goldsmiths_question(
    key: str, text: str, choices: dict = LIKERT_AGREE_7
) -> TextRangeQuestion:
    """Shorthand for creating a TextRangeQuestion with 7 answer options, in which the last answer of the choice set gives highest score"""
    return TextRangeQuestion(key=key, text=text, choices=choices, scoring_rule='LIKERT')


def goldsmiths_question_reversed(
    key: str, text: str, choices: dict = LIKERT_AGREE_7
) -> TextRangeQuestion:
    """Shorthand for creating a TextRangeQuestion with 7 answer options, in which the last answer of the choice set gives lowest score"""
    return TextRangeQuestion(
        key=key, text=text, choices=choices, scoring_rule='LIKERT_REVERSED'
    )


# Numbers before key relate to The Goldsmiths Musical Sophistication Index, v1.0
MSI_FG_GENERAL = [
    goldsmiths_question(
        key='msi_01_music_activities',
        text=_("I spend a lot of my free time doing music-related activities."),
    ),
    goldsmiths_question(
        key='msi_03_writing',
        text=_("I enjoy writing about music, for example on blogs and forums."),
    ),
    goldsmiths_question(
        key='msi_04_sing_along',
        text=_(
            "If somebody starts singing a song I don’t know, I can usually join in."
        ),
    ),
    goldsmiths_question(
        key='msi_07_from_memory', text=_("I can sing or play music from memory.")
    ),
    goldsmiths_question(
        key='msi_10_sing_with_recording',
        text=_("I am able to hit the right notes when I sing along with a recording."),
    ),
    goldsmiths_question(
        key='msi_12_performance_diff',
        text=_(
            "I can compare and discuss differences between two performances or versions of the same piece of music."
        ),
    ),
    goldsmiths_question_reversed(
        key='msi_14_never_complimented',
        text=_("I have never been complimented for my talents as a musical performer."),
    ),
    goldsmiths_question(
        key='msi_15_internet_search_music',
        text=_("I often read or search the internet for things related to music."),
    ),
    goldsmiths_question_reversed(
        key='msi_17_not_sing_harmony',
        text=_(
            "I am not able to sing in harmony when somebody is singing a familiar tune."
        ),
    ),
    goldsmiths_question(
        key='msi_19_identify_special',
        text=_("I am able to identify what is special about a given musical piece."),
    ),
    goldsmiths_question_reversed(
        key='msi_23_no_idea_in_tune',
        text=_("When I sing, I have no idea whether I’m in tune or not."),
    ),
    goldsmiths_question(
        key='msi_24_music_addiction',
        text=_("Music is kind of an addiction for me: I couldn’t live without it."),
    ),
    goldsmiths_question_reversed(
        key='msi_25_sing_public',
        text=_(
            "I don’t like singing in public because I’m afraid that I would sing wrong notes."
        ),
    ),
    goldsmiths_question_reversed(
        key='msi_27_consider_musician',
        text=_("I would not consider myself a musician."),
    ),
    goldsmiths_question(
        key='msi_29_sing_after_hearing',
        text=_(
            "After hearing a new song two or three times, I can usually sing it by myself."
        ),
    ),
    RadiosQuestion(
        key='msi_32_practice_years',
        text=_(
            "I engaged in regular, daily practice of a musical instrument (including voice) for _ years."
        ),
        choices=GMSI_YEARS_PRACTICED,
        scoring_rule='LIKERT',
    ),
    RadiosQuestion(
        key='msi_33_practice_daily',
        text=_(
            "At the peak of my interest, I practised my primary instrument for _ hours per day."
        ),
        choices=GMSI_HOURS_DAILY_PRACTICE,
        scoring_rule='LIKERT',
    ),
    RadiosQuestion(
        key='msi_37_play_instruments',
        text=_("How many musical instruments can you play?"),
        choices=GMSI_N_INSTRUMENTS,
        scoring_rule='LIKERT',
    ),
]

MSI_F1_ACTIVE_ENGAGEMENT = [
    question_by_key('msi_01_music_activities', MSI_FG_GENERAL),
    question_by_key('msi_03_writing', MSI_FG_GENERAL),
    goldsmiths_question(
        key='msi_08_intrigued_styles',
        text=_(
            "I’m intrigued by musical styles I’m not familiar with and want to find out more."
        ),
    ),
    question_by_key('msi_15_internet_search_music', MSI_FG_GENERAL),
    goldsmiths_question_reversed(
        key='msi_21_spend_income',
        text=_("I don’t spend much of my disposable income on music."),
    ),
    question_by_key('msi_24_music_addiction', MSI_FG_GENERAL),
    goldsmiths_question(
        key='msi_28_track_new',
        text=_(
            " I keep track of new music that I come across (e.g. new artists or recordings)."
        ),
    ),
    RadiosQuestion(
        key='msi_34_attended_events',
        text=_(
            "I have attended _ live music events as an audience member in the past twelve months."
        ),
        choices=GMSI_ATTENDED_EVENTS,
        scoring_rule='LIKERT',
    ),
    RadiosQuestion(
        key='msi_38_listen_music',
        text=_("I listen attentively to music for _ per day."),
        choices=GMSI_DAILY_MUSIC_LISTENING,
        scoring_rule='LIKERT',
    ),
]

MSI_F2_PERCEPTUAL_ABILITIES = [
    goldsmiths_question(
        key='msi_05_good_singer',
        text=_("I am able to judge whether someone is a good singer or not."),
    ),
    goldsmiths_question(
        key='msi_06_song_first_time',
        text=_("I usually know when I’m hearing a song for the first time."),
    ),
    goldsmiths_question_reversed(
        key='msi_11_spot_mistakes',
        text=_(
            "I find it difficult to spot mistakes in a performance of a song even if I know the tune."
        ),
    ),
    question_by_key('msi_12_performance_diff', MSI_FG_GENERAL),
    goldsmiths_question_reversed(
        key='msi_13_trouble_recognising',
        text=_(
            "I have trouble recognising a familiar song when played in a different way or by a different performer."
        ),
    ),
    goldsmiths_question(
        key='msi_18_out_of_beat',
        text=_("I can tell when people sing or play out of time with the beat."),
    ),
    goldsmiths_question(
        key='msi_22_out_of_tune',
        text=_("I can tell when people sing or play out of tune."),
    ),
    question_by_key('msi_23_no_idea_in_tune', MSI_FG_GENERAL),
    goldsmiths_question(
        key='msi_26_genre',
        text=_("When I hear a piece of music I can usually identify its genre."),
    ),
]

MSI_F3_MUSICAL_TRAINING = [
    question_by_key('msi_14_never_complimented', MSI_FG_GENERAL),
    question_by_key('msi_27_consider_musician', MSI_FG_GENERAL),
    question_by_key('msi_32_practice_years', MSI_FG_GENERAL),
    question_by_key('msi_33_practice_daily', MSI_FG_GENERAL),
    RadiosQuestion(
        key='msi_35_theory_training',
        text=_("I have had formal training in music theory for _ years."),
        choices=GMSI_YEARS_THEORY_TRAINING,
        scoring_rule='LIKERT',
    ),
    RadiosQuestion(
        key='msi_36_instrumental_training',
        text=_(
            "I have had _ years of formal training on a musical instrument (including voice) during my lifetime."
        ),
        choices=GMSI_YEARS_INSTRUMENTAL_TRAINING,
        scoring_rule='LIKERT',
    ),
    question_by_key('msi_37_play_instruments', MSI_FG_GENERAL),
]

MSI_F4_SINGING_ABILITIES = [
    question_by_key('msi_04_sing_along', MSI_FG_GENERAL),
    question_by_key('msi_07_from_memory', MSI_FG_GENERAL),
    question_by_key('msi_10_sing_with_recording', MSI_FG_GENERAL),
    question_by_key('msi_17_not_sing_harmony', MSI_FG_GENERAL),
    question_by_key('msi_25_sing_public', MSI_FG_GENERAL),
    question_by_key('msi_29_sing_after_hearing', MSI_FG_GENERAL),
    goldsmiths_question(
        key='msi_30_sing_back',
        text=_(
            "I only need to hear a new tune once and I can sing it back hours later."
        ),
    ),
]

MSI_F5_EMOTIONS = [
    goldsmiths_question(
        key='msi_02_shivers',
        text=_("I sometimes choose music that can trigger shivers down my spine."),
    ),
    goldsmiths_question_reversed(
        key='msi_09_rarely_emotions',
        text=_("Pieces of music rarely evoke emotions for me."),
    ),
    goldsmiths_question(
        key='msi_16_motivate',
        text=_("I often pick certain music to motivate or excite me."),
    ),
    question_by_key('msi_19_identify_special', MSI_FG_GENERAL),
    goldsmiths_question(
        key='msi_20_talk_emotions',
        text=_(
            "I am able to talk about the emotions that a piece of music evokes for me."
        ),
    ),
    goldsmiths_question(
        key='msi_31_memories',
        text=_("Music can evoke my memories of past people and places."),
    ),
]

MSI_OTHER = [
    TextQuestion(
        key='msi_39_best_instrument',
        text=_("The instrument I play best, including voice (or none), is:"),
    ),
    RadiosQuestion(
        key='ST_01_age_instrument',
        text=_("What age did you start to play an instrument?"),
        choices={
            '2 - 19': _('2 - 19'),
            'I don’t play any instrument.': _('I don’t play any instrument.'),
        },
    ),
    RadiosQuestion(
        key='AP_01_absolute_pitch',
        text=_(
            "Do you have absolute pitch? Absolute or perfect pitch is the ability to recognise and name an isolated musical tone without a reference tone, e.g. being able to say 'F#' if someone plays that note on the piano."
        ),
        choices={
            'yes': _('yes'),
            'no': _('no'),
        },
    ),
]

MSI_ALL = (
    MSI_F1_ACTIVE_ENGAGEMENT
    + MSI_F2_PERCEPTUAL_ABILITIES
    + MSI_F3_MUSICAL_TRAINING
    + MSI_F4_SINGING_ABILITIES
    + MSI_F5_EMOTIONS
)
