import logging
from .views import Final
from .util.score import SCORING_RULES

logger = logging.getLogger(__name__)

class Base(object):
    """Base class for other rules classes"""

    @classmethod
    def prepare_result(cls, session, section, expected_response=None):
        # Prevent circular dependency errors
        from experiment.models import Result

        result = Result(session=session)
        result.section = section
        if expected_response is not None:
            result.expected_response = expected_response
        result.save()
        return result.pk

    @classmethod
    def get_result(cls, session, result_id=None):
        from experiment.models import Result
        
        if not result_id:
            result = Result(session=session)
        try:
            result = Result.objects.get(pk=result_id, session=session)
        except Result.DoesNotExist:
            # Create new result
            result = Result(session=session)
        return result

    @classmethod
    def handle_results(cls, session, data):
        """ 
        if the given_result is an array of results, retrieve and save results for all of them
        """
        form = data.pop('form')
        for form_element in form:
            result = cls.get_result(session, form_element['result_id'])

            # Set given_response here, so it can be used in calculate_score
            result.given_response = form_element['value']
            
            # Calculate score
            score = session.experiment_rules().calculate_score(result, data, form_element)
            if not score:
                score = 0

            result.save_json_data(data)
            result.score = score
            result.save()
        return result

    @classmethod
    def handle_result(cls, session, data):
        """
        Create a result for given session, based on the result data and section_id

        parameters:
        session: a Session object
        data: a dictionary, containing an optional result_id, and optional other params:
        {
            result_id: int [optional] 
            ...
            all other params in the custom result
        }
        """

        result_id = data.get('result_id')
        result = cls.get_result(session, result_id)

        # Calculate score
        score = session.experiment_rules().calculate_score(result, data)
        if not score:
            score = 0

        # Populate and save the result
        result.save_json_data(data)
        result.score = score
        result.save()

        return result

    @classmethod
    def calculate_score(cls, result, data, form_element=None):
        """use scoring rule to calculate score
        If not scoring rule is defined, return None"""
        scoring_rule = SCORING_RULES.get(form_element['scoring_rule'], None)
        if scoring_rule:
            return scoring_rule(form_element, result, data)
        return None

    @staticmethod
    def final_score_message(session):
        """Create final score message for given session, base on score per result"""

        correct = 0
        total = 0

        for result in session.result_set.all():
            # if a result has score != 0, it was recognized
            if result.score:
                total += 1

                if result.score > 0:
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
