from .song_sync_only import SongSyncOnly
from .short_long import ShortLong
# from .short_long_tags import ShortLongTags
# from .demo import Demo
from .demo_taf import DemoTAF
from .demo_two_song import DemoTwoSong
from .eurovision_2020 import Eurovision2020
from .kuiper_2020 import Kuiper2020
from .beijaert_2021 import Beijaert2021
from .huang_2021 import Huang2021
from .beat_alignment import BeatAlignment
from .speech2song import Speech2Song
from .duration_discrimination import DurationDiscrimination
from .duration_discrimination_tone import DurationDiscriminationTone
from .anisochrony import Anisochrony
from .h_bat import HBat
from .hbat_bst import BST
from .rhythm_discrimination import RhythmDiscrimination
from .gold_msi import GoldMSI

# Rules available to this application
# If you create new Rules, add them to the list
# so they can be referred to by the admin

EXPERIMENT_RULES = {
    # Demo.ID: Demo,
    DemoTAF.ID: DemoTAF,
    DemoTwoSong.ID: DemoTwoSong,

    SongSyncOnly.ID: SongSyncOnly,
    ShortLong.ID: ShortLong,
    # ShortLongTags.ID: ShortLongTags,
    Eurovision2020.ID: Eurovision2020,
    Kuiper2020.ID: Kuiper2020,
    Beijaert2021.ID: Beijaert2021,
    Huang2021.ID: Huang2021,
    BeatAlignment.ID: BeatAlignment,
    Speech2Song.ID: Speech2Song,
    DurationDiscrimination.ID: DurationDiscrimination,
    DurationDiscriminationTone.ID: DurationDiscriminationTone,
    Anisochrony.ID: Anisochrony,
    HBat.ID: HBat,
    BST.ID: BST,
    RhythmDiscrimination.ID: RhythmDiscrimination,
    GoldMSI.ID: GoldMSI
}
