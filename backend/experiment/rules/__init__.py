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
from .h_bat_bfit import HBatBFIT
from .hbat_bst import BST
from .rhythm_discrimination import RhythmDiscrimination
from .rhythm_test_series import RhythmTestSeries
from .gold_msi import GoldMSI
from .listening_conditions import ListeningConditions

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
    HBatBFIT.ID: HBatBFIT,
    BST.ID: BST,
    RhythmDiscrimination.ID: RhythmDiscrimination,
    RhythmTestSeries.ID: RhythmTestSeries,
    GoldMSI.ID: GoldMSI,
    ListeningConditions.ID: ListeningConditions,
}
