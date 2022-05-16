from django.utils.translation import gettext_lazy as _

from experiment.rules.views.form import LikertQuestion, ChoiceQuestion
from .questions import question_by_key

# Numbers before key relate to The Goldsmiths Musical Sophistication Index, v1.0

MSI_FG_GENERAL = [
    LikertQuestion(
        key='msi_01_music_activities',
        question=_(
            "I spend a lot of my free time doing music-related activities.")),
    LikertQuestion(
        key='msi_03_writing',
        question=_(
            "I enjoy writing about music, for example on blogs and forums.")),
    LikertQuestion(
        key='msi_04_sing_along',
        question=_(
            "If somebody starts singing a song I don’t know, I can usually join in.")),
    LikertQuestion(
        key='msi_07_from_memory',
        question=_("I can sing or play music from memory.")),
    LikertQuestion(
        key='msi_10_sing_with_recording',
        question=_(
            "I am able to hit the right notes when I sing along with a recording.")),
    LikertQuestion(
        key='msi_12_performance_diff',
        question=_(
            "I can compare and discuss differences between two performances or versions of the same piece of music."),
        ),
    LikertQuestion(
        key='msi_14_never_complimented',
        question=_(
            "I have never been complimented for my talents as a musical performer.")),
    LikertQuestion(
        key='msi_15_internet_search_music',
        question=_(
            "I often read or search the internet for things related to music.")),
    LikertQuestion(
        key='msi_17_not_sing_harmony',
        question=_(
            "I am not able to sing in harmony when somebody is singing a familiar tune.")),
    LikertQuestion(
        key='msi_19_identify_special',
        question=_(
            "I am able to identify what is special about a given musical piece.")),
    LikertQuestion(
        key='msi_23_no_idea_in_tune',
        question=_("When I sing, I have no idea whether I’m in tune or not.")),
    LikertQuestion(
        key='msi_24_music_addiction',
        question=_(
            "Music is kind of an addiction for me: I couldn’t live without it.")),
    LikertQuestion(
        key='msi_25_sing_public',
        question=_(
            "I don’t like singing in public because I’m afraid that I would sing wrong notes.")),
    LikertQuestion(
        key='msi_27_consider_musician',
        question=_("I would not consider myself a musician.")),
    LikertQuestion(
        key='msi_29_sing_after_hearing',
        question=_(
            "After hearing a new song two or three times, I can usually sing it by myself.")),
    ChoiceQuestion(
        key='msi_32_practice_years',
        question=_(
            "I engaged in regular, daily practice of a musical instrument (including voice) for:"),
        choices={
            '0': _('0 years'),
            '1': _('1 year'),
            '2': _('2 years'),
            '3': _('3 years'),
            '4-5': _('4–5 years'),
            '6-9': _('6–9 years'),
            '10+': _('10 or more years'),
        },
        view='RADIOS'
    ),
    ChoiceQuestion(
        key='msi_33_practice_daily',
        question=_(
            "At the peak of my interest, I practiced on my primary instrument each day for:"),
        choices={
            '0': _('0 hours'),
            '0.5': _('0.5 hours'),
            '1': _('1 hour'),
            '1.5': _('1.5 hours'),
            '2': _('2 hours'),
            '3-4': _('3-4 hours'),
            '5+': _('5 or more hours'),
        },
        view='RADIOS'
    ),
    ChoiceQuestion(
        key='msi_37_play_instruments',
        question=_("How many musical instruments can you play?"),
        choices={
            '0': _('0'),
            '1': _('1'),
            '2': _('2'),
            '3': _('3'),
            '4': _('4'),
            '5': _('5'),
            '6+': _('6 or more'),
        },
        view='RADIOS'
    )
]

MSI_F1_ACTIVE_ENGAGEMENT = [
    question_by_key('msi_01_music_activities', MSI_FG_GENERAL),
    question_by_key('msi_03_writing', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_08_intrigued_styles',
        question=_(
            "I’m intrigued by musical styles I’m not familiar with and want to find out more.")),
    question_by_key('msi_15_internet_search_music', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_21_spend_income',
        question=_("I don’t spend much of my disposable income on music.")),
    question_by_key('msi_24_music_addiction', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_28_track_new',
        question=_(
            " I keep track of new music that I come across (e.g. new artists or recordings).")),
    ChoiceQuestion(
        key='msi_34_attended_events',
        question=_(
            "How many live music events have you attended as an audience member in the past twelve months?"),
        choices={
            '0.0': _('0'),
            '1.0': _('1'),
            '2.0': _('2'),
            '3.0': _('3'),
            '4-6': _('4-6'),
            '7-10': _('7-10'),
            '11+': _('11 or more'),
        },
        view='RADIOS'
    ),
    ChoiceQuestion(
        key='msi_38_listen_music',
        question=_(
            "How much time per day do you spend listening to music attentively?"),
        choices={
            '0-15': _('0-15 min'),
            '15-30': _('15-30 min'),
            '30-60': _('30-60 min'),
            '60-90': _('60-90 min'),
            '2h': _('2 hrs'),
            '2-3h': _('2-3 hrs'),
            '4h+': _('4 hrs or more'),
        },
        view='RADIOS'
    )
]

MSI_F2_PERCEPTUAL_ABILITIES = [
    LikertQuestion(
        key='msi_05_good_singer',
        question=_("I am able to judge whether someone is a good singer or not.")),
    LikertQuestion(
        key='msi_06_song_first_time',
        question=_("I usually know when I’m hearing a song for the first time.")),
    LikertQuestion(
        key='msi_11_spot_mistakes',
        question=_("I find it difficult to spot mistakes in a performance of a song even if I know the tune.")),
    question_by_key('msi_12_performance_diff', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_13_trouble_recognising',
        question=_(
            "I have trouble recognising a familiar song when played in a different way or by a different performer."),
        ),
    LikertQuestion(
        key='msi_18_out_of_beat',
        question=_(
            "I can tell when people sing or play out of time with the beat."),
        ),
    LikertQuestion(
        key='msi_22_out_of_tune',
        question=_("I can tell when people sing or play out of tune."),
        ),
    question_by_key('msi_23_no_idea_in_tune', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_26_genre',
        question=_(
            "When I hear a piece of music I can usually identify its genre."),
        )
]

MSI_F3_MUSICAL_TRAINING = [
    question_by_key('msi_14_never_complimented', MSI_FG_GENERAL),
    question_by_key('msi_27_consider_musician', MSI_FG_GENERAL),
    question_by_key('msi_32_practice_years', MSI_FG_GENERAL),
    question_by_key('msi_33_practice_daily', MSI_FG_GENERAL),
    ChoiceQuestion(
        key='msi_35_theory_training',
        question=_(
            "How many years of formal training have you had in music theory?"),
        choices={
            # use floats as key, to prevent int conversions while dumping json
            '0': _('0'),
            '0.5': _('0.5'),
            '1': _('1'),
            '2': _('2'),
            '3': _('3'),
            '4-6': _('4-6'),
            '7+': _('7 or more'),
        },
        view='RADIOS'
    ),
    ChoiceQuestion(
        key='msi_36_instrumental_training',
        question=_(
            "How many years of formal training have you had on a musical instrument (including voice) during your lifetime?"),
        choices={
            # use floats as key, to prevent int conversions while dumping json
            '0': _('0'),
            '0.5': _('0.5'),
            '1': _('1'),
            '2': _('2'),
            '3-5': _('3-5'),
            '6-9': _('6-9'),
            '10+': _('10 or more'),
        },
        view='RADIOS'
    ),
    question_by_key('msi_37_play_instruments', MSI_FG_GENERAL)
]

MSI_F4_SINGING_ABILITIES = [
    question_by_key('msi_04_sing_along', MSI_FG_GENERAL),
    question_by_key('msi_07_from_memory', MSI_FG_GENERAL),
    question_by_key('msi_10_sing_with_recording', MSI_FG_GENERAL),
    question_by_key('msi_17_not_sing_harmony', MSI_FG_GENERAL),
    question_by_key('msi_25_sing_public', MSI_FG_GENERAL),
    question_by_key('msi_29_sing_after_hearing', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_30_sing_back',
        question=_(
            "I only need to hear a new tune once and I can sing it back hours later."),
        )
]

MSI_F5_EMOTIONS = [
    LikertQuestion(
        key='msi_02_shivers',
        question=_(
            "I sometimes choose music that can trigger shivers down my spine."),
        ),
    LikertQuestion(
        key='msi_09_rarely_emotions',
        question=_("Pieces of music rarely evoke emotions for me."),
        ),
    LikertQuestion(
        key='msi_16_motivate',
        question=_("I often pick certain music to motivate or excite me."),
        ),
    question_by_key('msi_19_identify_special', MSI_FG_GENERAL),
    LikertQuestion(
        key='msi_20_talk_emotions',
        question=_(
            "I am able to talk about the emotions that a piece of music evokes for me."),
        ),
    LikertQuestion(
        key='msi_31_memories',
        question=_("Music can evoke my memories of past people and places."),
        )
]

MSI_ALL = (
    MSI_F1_ACTIVE_ENGAGEMENT
    + MSI_F2_PERCEPTUAL_ABILITIES
    + MSI_F3_MUSICAL_TRAINING
    + MSI_F4_SINGING_ABILITIES
    + MSI_F5_EMOTIONS
)
