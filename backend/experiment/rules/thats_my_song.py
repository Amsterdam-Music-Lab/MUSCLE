from django.utils.translation import gettext_lazy as _

from experiment.actions import Trial
from experiment.actions.form import Form
from experiment.questions.utils import question_by_key, unasked_question
from experiment.questions.musicgens import MUSICGENS_17_W_VARIANTS
from .hooked import Hooked

class ThatsMySong(Hooked):

	ID = 'THATS_MY_SONG'

	
	@classmethod
	def get_random_question(cls, session):
		demographics = [question_by_key('dgf_generation'), question_by_key('dgf_gender_identity')]
		question = unasked_question(
                session.participant,
                demographics
            )
		if question is None:
			question = unasked_question(
				session.participant,
				MUSICGENS_17_W_VARIANTS,
				randomize=True
			)
		
		if question is None:
			return None
		
		return Trial(
                title=_("Questionnaire"),
                feedback_form=Form([question], is_profile=True, is_skippable=question.is_skippable)).action()
