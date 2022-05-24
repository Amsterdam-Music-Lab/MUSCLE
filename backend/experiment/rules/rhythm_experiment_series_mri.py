from . import RhythmExperimentSeries

class RhythmExperimentSeriesMRI(RhythmExperimentSeries):
    ID = 'RHYTHM_SERIES_MRI'
    consent_form = 'consent/consent_rhythm_mri.html'
    debrief_form = 'final/experiment_series_mri.html'
