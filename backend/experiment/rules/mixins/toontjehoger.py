from session.models import Session

class ToontjeHogerMixin(object):
    """ The ToontjeHogerMixin provides methods used by all Toontjehoger rules """
    SCORE_CORRECT = 42 # override this per ruleset
    SCORE_WRONG = 0

    def calculate_score(self, result, data) -> int:
        score = self.SCORE_CORRECT if result.expected_response == result.given_response else self.SCORE_WRONG
        return score
    
    def get_final_statistics(self, session: Session) -> dict:
        return {"final_score": session.final_score}