from .demographics import DEMOGRAPHICS, EXTRA_DEMOGRAPHICS
from .goldsmiths import MSI_F1_ACTIVE_ENGAGEMENT, MSI_F2_PERCEPTUAL_ABILITIES, MSI_F3_MUSICAL_TRAINING, MSI_F4_SINGING_ABILITIES, MSI_F5_EMOTIONS, MSI_OTHER
from .languages import LANGUAGE
from .musicgens import MUSICGENS_17_W_VARIANTS
from .stomp import STOMP
from .tipi import TIPI
from .other import OTHER

# Label of the group as it will apear in the admin
QUESTION_GROUPS = [ ("DEMOGRAPHICS",DEMOGRAPHICS),
    ("EXTRA_DEMOGRAPHICS",EXTRA_DEMOGRAPHICS),
    ("MSI_F1_ACTIVE_ENGAGEMENT",MSI_F1_ACTIVE_ENGAGEMENT),
    ("MSI_F2_PERCEPTUAL_ABILITIES",MSI_F2_PERCEPTUAL_ABILITIES),
    ("MSI_F3_MUSICAL_TRAINING",MSI_F3_MUSICAL_TRAINING),
    ("MSI_F4_SINGING_ABILITIES",MSI_F4_SINGING_ABILITIES),
    ("MSI_F5_EMOTIONS",MSI_F5_EMOTIONS),
    ("MSI_OTHER",MSI_OTHER),
    ("LANGUAGE",LANGUAGE),
    ("MUSICGENS_17_W_VARIANTS",MUSICGENS_17_W_VARIANTS),
    ("STOMP",STOMP),
    ("TIPI",TIPI),
    ("OTHER",OTHER)
]

QUESTIONS_ALL = []
KEYS_ALL = []
QUESTIONS_CHOICES = []

for question_group in QUESTION_GROUPS:
    QUESTIONS_ALL.extend(question_group[1])
    KEYS_ALL.extend([question.key for question in question_group[1]])
    QUESTIONS_CHOICES.append( (question_group[0], [(q.key,"("+q.key+") "+q.question) for q in question_group[1]]) )

def get_default_question_keys():
    return []


def get_questions_from_keys(keys):
    """ Returns questions in the order of keys"""
    return [QUESTIONS_ALL[KEYS_ALL.index(key)] for key in keys]

if len(KEYS_ALL) != len(set(KEYS_ALL)):
    raise Exception("Duplicate question keys")
