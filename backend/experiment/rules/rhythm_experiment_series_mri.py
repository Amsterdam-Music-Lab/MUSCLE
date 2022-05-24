from . import RhythmExperimentSeries

class RhythmExperimentSeriesMRI(RhythmExperimentSeries):
    ID = 'RHYTHM_SERIES_MRI'
    consent_form = 'consent/consent_MRI.html'
    debrief_form = 'final/debrief_MRI.html'
