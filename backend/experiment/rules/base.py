import logging
from .views import Final
from .util.score import SCORING_RULES

logger = logging.getLogger(__name__)

class Base(object):
    """Base class for other rules classes"""

    @classmethod
    def prepare_result(cls, session, section, expected_response=None, scoring_rule='', comment=None):
        # Prevent circular dependency errors
        from experiment.models import Result, Score

        score = Score(rule=scoring_rule)
        score.save()
        result = Result(session=session, score_model=score)
        result.section = section
        if expected_response is not None:
            result.expected_response = expected_response
        if comment is not None:
            result.comment = comment
        result.save()
        return result.pk
    
    @classmethod
    def prepare_profile(cls, participant, key, scoring_rule=''):
        from experiment.models import Profile, Score
        try:
            profile = Profile.objects.get(
                participant=participant, question=key)
            # Existing profile value

        except Profile.DoesNotExist:
            # Create new profile value
            score = Score(rule=scoring_rule)
            score.save()
            profile = Profile(
                participant=participant,
                question=key,
                score_model=score
            )
            profile.save()

    @classmethod
    def get_result(cls, session, data):
        from experiment.models import Result, Score
        
        result_id = data.get('result_id')
        try:
            result = Result.objects.get(pk=result_id, session=session)
        except Result.DoesNotExist:
            # Create new result
            score = Score()
            score.save()
            result = Result(session=session, score_model=score)
        return result

    @classmethod
    def handle_results(cls, session, data):
        """ 
        if the given_result is an array of results, retrieve and save results for all of them
        else, handle results at top level
        """
        form = data.get('form')
        if not form:
            # handle results at top level
            return cls.score_result(session, data)
        for form_element in form:
            result = cls.score_result(session, form_element)
        return result

    @classmethod
    def score_result(cls, session, data):
        """
        Create a result for given session, based on the result data 
        (form element or top level data)

        parameters:
        session: a Session object
        data: a dictionary, containing an optional result_id, and optional other params:
        {
            result_id: int [optional]
            params: ...
        }
        """
        result = cls.get_result(session, data)
        result.given_response = data.get('value')

        # Calculate score        
        score = session.experiment_rules().calculate_score(result, data)
        if not score:
            score = 0

        # Populate and save the result
        result.save_json_data(data)
        result.score_model.value = score
        result.score_model.save()
        result.save()

        return result

    @classmethod
    def calculate_score(cls, result, data):
        """use scoring rule to calculate score
        If not scoring rule is defined, return None"""
        score = result.score_model
        scoring_rule = SCORING_RULES.get(score.rule)
        if scoring_rule:
            return scoring_rule(result, data)
        return None

    @staticmethod
    def final_score_message(session):
        """Create final score message for given session, base on score per result"""

        correct = 0
        total = 0

        for result in session.result_set.all():
            # if a result has score != 0, it was recognized
            if result.score_model.value:
                total += 1

                if result.score_model.value > 0:
                    # if a result has score > 0, it was identified correctly
                    correct += 1

        score_message = "Well done!" if session.final_score > 0 else "Too bad!"
        message = "You correctly identified {} out of {} recognized songs!".format(
            correct,
            total
        )
        return score_message + " " + message

    @staticmethod
    def rank(session):
        """Get rank based on session score"""
        score = session.final_score
        ranks = Final.RANKS

        # Few or negative points or no score, always return lowest plastic score
        if score <= 0 or not score:
            return ranks['PLASTIC']

        # Buckets for positive scores:
        # rank: starts percentage
        buckets = [
            # ~ stanines 1-3
            {'rank': ranks['BRONZE'],   'min_percentile':   0.0},
            # ~ stanines 4-6
            {'rank': ranks['SILVER'],   'min_percentile':  25.0},
            # ~ stanine 7
            {'rank': ranks['GOLD'],     'min_percentile':  75.0},
            {'rank': ranks['PLATINUM'],
                'min_percentile':  90.0},   # ~ stanine 8
            {'rank': ranks['DIAMOND'],
                'min_percentile':  95.0},   # ~ stanine 9
        ]

        percentile = session.percentile_rank()

        # Check the buckets in reverse order
        # If the percentile rank is higher than the min_percentile
        # return the rank
        for bucket in reversed(buckets):
            if percentile >= bucket['min_percentile']:
                return bucket['rank']

        # Default return, in case score isn't in the buckets
        return ranks['PLASTIC']
