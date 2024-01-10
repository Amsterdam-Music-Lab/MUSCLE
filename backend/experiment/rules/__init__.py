from .beat_alignment import BeatAlignment
from .duration_discrimination import DurationDiscrimination
from .duration_discrimination_tone import DurationDiscriminationTone
from .anisochrony import Anisochrony
from .categorization import Categorization
from .eurovision_2020 import Eurovision2020
from .gold_msi import GoldMSI
from .h_bat import HBat
from .h_bat_bfit import HBatBFIT
from .hbat_bst import BST
from .hooked import Hooked
from .tele_tunes import HookedTeleTunes
from .huang_2022 import Huang2022
from .kuiper_2020 import Kuiper2020
from .listening_conditions import ListeningConditions
from .matching_pairs import MatchingPairs
from .matching_pairs_icmpc import MatchingPairsICMPC
from .musical_preferences import MusicalPreferences
from .rhythm_discrimination import RhythmDiscrimination
from .rhythm_experiment_series import RhythmExperimentSeries
from .rhythm_experiment_series_mri import RhythmExperimentSeriesMRI
from .rhythm_experiment_series_unpaid import RhythmExperimentSeriesUnpaid
from .speech2song import Speech2Song
from .thats_my_song import ThatsMySong
from .toontjehoger_home import ToontjeHogerHome
from .toontjehoger_1_mozart import ToontjeHoger1Mozart
from .toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from .toontjehoger_3_plink import ToontjeHoger3Plink
from .toontjehoger_4_absolute import ToontjeHoger4Absolute
from .toontjehoger_5_tempo import ToontjeHoger5Tempo
from .toontjehoger_6_relative import ToontjeHoger6Relative
from .visual_matching_pairs import VisualMatchingPairs

# Rules available to this application
# If you create new Rules, add them to the list
# so they can be referred to by the admin

EXPERIMENT_RULES = {
    BeatAlignment.ID: BeatAlignment,
    Speech2Song.ID: Speech2Song,
    DurationDiscrimination.ID: DurationDiscrimination,
    DurationDiscriminationTone.ID: DurationDiscriminationTone,
    Anisochrony.ID: Anisochrony,
    HBat.ID: HBat,
    HBatBFIT.ID: HBatBFIT,
    BST.ID: BST,
    Hooked.ID: Hooked,
    HookedTeleTunes.ID: HookedTeleTunes,
    MatchingPairs.ID: MatchingPairs,
    MatchingPairsICMPC.ID: MatchingPairsICMPC,
    MusicalPreferences.ID: MusicalPreferences,
    RhythmDiscrimination.ID: RhythmDiscrimination,
    RhythmExperimentSeries.ID: RhythmExperimentSeries,
    RhythmExperimentSeriesMRI.ID: RhythmExperimentSeriesMRI,
    RhythmExperimentSeriesUnpaid.ID: RhythmExperimentSeriesUnpaid,
    GoldMSI.ID: GoldMSI,
    ListeningConditions.ID: ListeningConditions,
    Huang2022.ID: Huang2022,
    Categorization.ID: Categorization,
    ToontjeHogerHome.ID: ToontjeHogerHome,
    ToontjeHoger1Mozart.ID: ToontjeHoger1Mozart,
    ToontjeHoger2Preverbal.ID: ToontjeHoger2Preverbal,
    ToontjeHoger3Plink.ID: ToontjeHoger3Plink,
    ToontjeHoger4Absolute.ID: ToontjeHoger4Absolute,
    ToontjeHoger5Tempo.ID: ToontjeHoger5Tempo,
    ToontjeHoger6Relative.ID: ToontjeHoger6Relative,
    Eurovision2020.ID: Eurovision2020,
    Kuiper2020.ID: Kuiper2020,
    ThatsMySong.ID: ThatsMySong
}
