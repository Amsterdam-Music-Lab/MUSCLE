from django.utils.translation import gettext_lazy as _

from experiment.actions.form import LikertQuestion, RadiosQuestion

def frequency_question(key, question):
    """Define a question with frequency options"""
    return LikertQuestion(
        key = key,
        question = question,
        choices = {
            1: _("Never"),
            2: _("Not very often"),
            3: _("Occasionally"),
            4: _("Sometimes"),
            5: _("Very often"),
            6: _("Always")
        },
        explainer = _("Please tell us how much you agree")
    )

def agreement_question(key, question):
    """Define a question with agreement options"""
    return LikertQuestion(
        key = key,
        question = question,
        choices = {
            1: _("Completely disagree"),
            2: _("Strongly disagree"),
            3: _("Disagree"),
            4: _("Neither agree or disagree"),
            5: _("Agree"),
            6: _("Strongly agree"),
            7: _("Completely agree")
        },
        explainer = _("Please tell us how much you agree")
    )

THATS_MY_SONG_QUESTIONS_FIXED = [
    frequency_question("VB_01", _("I can sing or play a song from memory.")),
    frequency_question(
        "VB_02",
        _("I can tell when people sing or play out of time with the beat of music."),
    ),
    frequency_question(
        "VB_03", _("I can recognize a piece of music after hearing just a few notes.")
    ),
    agreement_question("VB_04", _("My musical ability is important to my identity.")),
    agreement_question("VB_05", _("Listening to music makes me feel less alone.")),
]
THATS_MY_SONG_QUESTIONS_RANDOM = [
    frequency_question("VB_06", _("I can tell when people sing out of tune.")),
    frequency_question("VB_07", _("Music gives me shivers or goosebumps.")),
    frequency_question("VB_08", _("I lose myself in music.")),
    frequency_question(
        "VB_09",
        _("I am able to hit the right notes when I sing along with a recording."),
    ),
    frequency_question(
        "VB_10", _("I have a piece of music stuck on repeat in my head.")
    ),
    frequency_question("VB_11", _("Music makes me dance.")),
    agreement_question("VB_12", _("I can tap in time with a musical beat.")),
    agreement_question(
        "VB_13",
        _("I have never been complimented for my talents as a musical performer."),
    ),
    agreement_question(
        "VB_14",
        _(
            "When I feel anxious, listening to music helps me see things in a more positive light."
        ),
    ),
    agreement_question(
        "VB_15", _("Making music helps me to socially connect with others.")
    ),
]
