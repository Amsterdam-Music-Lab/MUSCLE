import logging

from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from experiment.actions import Final
from result.score import SCORING_RULES


logger = logging.getLogger(__name__)

class Base(object):
    """Base class for other rules classes"""

    contact_email = settings.CONTACT_MAIL

    @classmethod
    def feedback_info(cls):
        feedback_body = render_to_string('feedback/user_feedback.html', {'email': cls.contact_email})
        return {
            'header': _("Do you have any remarks or questions?"),
            'button': _("Submit"),
            'contact_body': feedback_body,
            'thank_you': _("We appreciate your feedback!")
        }

    @classmethod
    def calculate_score(cls, result, data):
        """use scoring rule to calculate score
        If not scoring rule is defined, return None
        Override in rules file for other scoring schemes"""
        scoring_rule = SCORING_RULES.get(result.scoring_rule)
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
    def rank(session, exclude_unfinished=True):
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

        percentile = session.percentile_rank(exclude_unfinished)

        # Check the buckets in reverse order
        # If the percentile rank is higher than the min_percentile
        # return the rank
        for bucket in reversed(buckets):
            if percentile >= bucket['min_percentile']:
                return bucket['rank']

        # Default return, in case score isn't in the buckets
        return ranks['PLASTIC']
