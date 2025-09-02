from .anisochrony import Anisochrony
from .beat_alignment import BeatAlignment
from .categorization import Categorization
from .congosamediff import CongoSameDiff
from .duration_discrimination import DurationDiscrimination
from .duration_discrimination_tone import DurationDiscriminationTone
from .eurovision_2020 import Eurovision2020
from .h_bat import HBat
from .h_bat_bfit import HBatBFIT
from .hbat_bst import BST
from .hooked import Hooked
from .huang_2022 import Huang2022
from .kuiper_2020 import Kuiper2020
from .matching_pairs import MatchingPairsGame
from .matching_pairs_fixed import MatchingPairsFixed
from .matching_pairs_lite import MatchingPairsLite
from .matching_pairs_icmpc import MatchingPairsICMPC
from .matching_pairs_2025 import MatchingPairs2025
from .musical_preferences import MusicalPreferences
from .questionnaire import Questionnaire
from .rhythm_battery_final import RhythmBatteryFinal
from .rhythm_battery_intro import RhythmBatteryIntro
from .rhythm_discrimination import RhythmDiscrimination
from .speech2song import Speech2Song
from .tele_tunes import HookedTeleTunes
from .thats_my_song import ThatsMySong
from .toontjehoger_1_mozart import ToontjeHoger1Mozart
from .toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from .toontjehoger_3_plink import ToontjeHoger3Plink
from .toontjehoger_4_absolute import ToontjeHoger4Absolute
from .toontjehoger_5_tempo import ToontjeHoger5Tempo
from .toontjehoger_6_relative import ToontjeHoger6Relative
from .tafc import TwoAlternativeForced
from .toontjehogerkids_1_mozart import ToontjeHogerKids1Mozart
from .toontjehogerkids_2_preverbal import ToontjeHogerKids2Preverbal
from .toontjehogerkids_3_plink import ToontjeHogerKids3Plink
from .toontjehogerkids_4_absolute import ToontjeHogerKids4Absolute
from .toontjehogerkids_5_tempo import ToontjeHogerKids5Tempo
from .toontjehogerkids_6_relative import ToontjeHogerKids6Relative

# Rules available to this application
# If you create new Rules, add them to the list
# so they can be referred to by the admin

BLOCK_RULES = {
    Anisochrony.ID: Anisochrony,
    BeatAlignment.ID: BeatAlignment,
    BST.ID: BST,
    Categorization.ID: Categorization,
    CongoSameDiff.ID: CongoSameDiff,
    DurationDiscrimination.ID: DurationDiscrimination,
    DurationDiscriminationTone.ID: DurationDiscriminationTone,
    Eurovision2020.ID: Eurovision2020,
    HBat.ID: HBat,
    HBatBFIT.ID: HBatBFIT,
    Hooked.ID: Hooked,
    HookedTeleTunes.ID: HookedTeleTunes,
    Huang2022.ID: Huang2022,
    Kuiper2020.ID: Kuiper2020,
    MatchingPairsFixed.ID: MatchingPairsFixed,
    MatchingPairsGame.ID: MatchingPairsGame,
    MatchingPairsLite.ID: MatchingPairsLite,
    MatchingPairsICMPC.ID: MatchingPairsICMPC,
    MatchingPairs2025.ID: MatchingPairs2025,
    MusicalPreferences.ID: MusicalPreferences,
    Questionnaire.ID: Questionnaire,
    RhythmBatteryFinal.ID: RhythmBatteryFinal,
    RhythmBatteryIntro.ID: RhythmBatteryIntro,
    RhythmDiscrimination.ID: RhythmDiscrimination,
    TwoAlternativeForced.ID: TwoAlternativeForced,
    Speech2Song.ID: Speech2Song,
    ThatsMySong.ID: ThatsMySong,
    ToontjeHoger1Mozart.ID: ToontjeHoger1Mozart,
    ToontjeHoger2Preverbal.ID: ToontjeHoger2Preverbal,
    ToontjeHoger3Plink.ID: ToontjeHoger3Plink,
    ToontjeHoger4Absolute.ID: ToontjeHoger4Absolute,
    ToontjeHoger5Tempo.ID: ToontjeHoger5Tempo,
    ToontjeHoger6Relative.ID: ToontjeHoger6Relative,
    ToontjeHogerKids1Mozart.ID: ToontjeHogerKids1Mozart,
    ToontjeHogerKids2Preverbal.ID: ToontjeHogerKids2Preverbal,
    ToontjeHogerKids3Plink.ID: ToontjeHogerKids3Plink,
    ToontjeHogerKids4Absolute.ID: ToontjeHogerKids4Absolute,
    ToontjeHogerKids5Tempo.ID: ToontjeHogerKids5Tempo,
    ToontjeHogerKids6Relative.ID: ToontjeHogerKids6Relative,
}
