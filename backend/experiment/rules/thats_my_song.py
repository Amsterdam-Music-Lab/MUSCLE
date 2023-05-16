from django.utils.translation import gettext_lazy as _

from experiment.actions import Trial
from experiment.actions.form import Form
from experiment.questions.utils import question_by_key, unasked_question
from experiment.questions.musicgens import MUSICGENS_17_W_VARIANTS
from .hooked import Hooked

class ThatsMySong(Hooked):

	ID = 'THATS_MY_SONG'
	consent_file = None

	
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
                feedback_form=Form([question], is_skippable=question.is_skippable)).action()

	def get_info_playlist(self, filename):
		parts = filename.split(' - ')
		time_info = int(parts[0])
		if time_info < 1970:
			decade = '1960s'
		elif time_info < 1980:
			decade = '1970s'
		elif time_info < 1990:
			decade = '1980s'
		elif time_info < 2000:
			decade = '1990s'
		else:
			decade = '2000s'
		try:
			int(parts[-1])
			form = parts[-2]
		except:
			form = parts[-1]
		return {
			'artist': parts[1],
			'song': parts[2],
			'tag': form,
			'group': decade
		}

