import random
import uuid

from django.contrib.humanize.templatetags.humanize import naturalday
from django.db import models


class Participant(models.Model):
    """Main participant, base for profile and sessions"""

    unique_hash = models.CharField(
        max_length=64, unique=True, default=uuid.uuid4)
    country_code = models.CharField(max_length=3, default="")
    access_info = models.CharField(max_length=512, default="", null=True)
    participant_id_url = models.CharField(max_length=128, null=True, unique=True)

    def __str__(self):
        return "Participant {}".format(self.id)

    def session_count(self):
        """Get number of sessions"""
        return self.session_set.count()

    session_count.short_description = 'Sessions'

    def result_count(self):
        """Get total number of results"""
        c = 0
        for session in self.session_set.all():
            c += session.result_set.count()
        return c

    result_count.short_description = 'Results'

    def export_admin(self):
        """Export data to admin"""
        return {
            "id": self.id,
            "unique_hash": self.unique_hash,
            "country_code": self.country_code,
            "access_info": self.access_info,
            "participant_id_url": self.participant_id_url,
            "profile": self.profile_object()
        }

    def export_profiles(self):
        # export participant profile result objects
        return self.result_set.all()

    def profile(self):
        """Get all answered results of this participant"""
        return self.result_set.all().filter(given_response__isnull=False)

    def profile_object(self):
        """Get full profile data"""
        profile_object = {}
        for profile in self.profile():
            profile_object[profile.question_key] = profile.given_response
            if profile.score:
                profile_object['{}_score'.format(
                    profile.question_key)] = profile.score
        return profile_object

    def is_dutch(self):
        """Return if participant is tagged with Netherlands (nl) country code"""
        return self.country_code == "nl"

    def scores_per_experiment(self):
        """Scores per finished experiment session"""
        scores = []

        # Get all finished sessions
        sessions = self.session_set.exclude(
            finished_at=None).order_by('-final_score')

        hits = {}

        # Create best rank/score data per experiment session
        for session in sessions:

            if session.experiment.slug in hits:
                continue

            hits[session.experiment.slug] = True

            scores.append({
                'experiment_slug': session.experiment.slug,
                'experiment_name': session.experiment.name,
                'rank': session.experiment.get_rules().rank(session),
                'score': session.final_score,
                'date': naturalday(session.finished_at),
            })

        return scores
