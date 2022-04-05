from .views.playback import Playback
from .views.form import Form, Question
from .views.trial import Trial

class Categorization(Base):

    def first_round():
        # Consent
        # StartSession
        # check which group participant belongs to
        # set assignment blue / orange etc.
        # save to session.json_data

    def next_round(session):
        # logic for retrieving sections
        section = session.playlists.all().get()
        # during debugging: display the filename
        playback = Playback('BUTTON', [section])
        # retrieve expected response from json_data
        result_pk = Result(expected_response='A')
        # during debugging: display correct / incorrect on buttons
        question = ChoiceQuestion('categorize', 'BUTTON_ARRAY', result_id=result_pk)
        form = Form([question])
        view = Trial(playback=playback, feedback_form=form)
        return view

    def get_trial_with_feedback(session):
        explainer = Explainer()
        trial = Trial()
        return combine_actions(explainer, trial)