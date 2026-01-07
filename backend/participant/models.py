import uuid

from django.contrib.humanize.templatetags.humanize import naturalday
from django.db import models
from django.db.models.query import QuerySet
from question.models import QuestionGroup
from django.db.models import Sum
from result.models import Result


class PartipantManager(models.Manager):

    def with_accumulative_score(self):
        return self.annotate(accumulative_score=Sum("session__final_score", default=0))


class Participant(models.Model):
    """Main participant, base for profile and sessions

    Attributes:
        unique_hash (str): Unique identifier string
        country_code (str): Country code of the participant
        access_info (str): HTTP_USER_AGENT info
        participant_id_url (str): URL code to link an experiment to a participant
    """

    unique_hash = models.CharField(
        max_length=64, unique=True, default=uuid.uuid4)
    country_code = models.CharField(max_length=3, default="")
    access_info = models.CharField(max_length=512, default="", null=True)
    participant_id_url = models.CharField(max_length=128, null=True, unique=True)
    objects = PartipantManager()

    def __str__(self):
        return "Participant {}".format(self.id)

    def session_count(self) -> int:
        """Get the total number of started sessions by this participant

        Returns:
            Number of started sessions by a Participant

        Example:
            Get the number of started sessions by this Participant
            ```python
            session_count = participant.session_count()
            ```
        """
        return self.session_set.count()

    session_count.short_description = 'Sessions'

    def percentile_rank_accumulative_score(self) -> float:
        all_participants = Participant.objects.with_accumulative_score()
        this_score = all_participants.get(pk=self.pk).accumulative_score
        n_participants = all_participants.count()
        n_lte = all_participants.filter(accumulative_score__lte=this_score).count()
        n_eq = all_participants.filter(accumulative_score=this_score).count()
        return 100.0 * (n_lte - (0.5 * n_eq)) / n_participants

    def result_count(self) -> int:
        """Get the total number of results

        Returns:
            Total number of results from all the sessions by a Participant

        Example:
            Get the number of results from this Participant
            ```python
            result_count = participant.result_count()
            ```
        """
        c = 0
        for session in self.session_set.all():
            c += session.result_set.count()
        return c

    result_count.short_description = 'Results'

    def _export_admin(self)  -> dict:
        """Export data to admin

        Returns:
            Participant data for admin
        """
        return {
            "id": self.id,
            "unique_hash": self.unique_hash,
            "country_code": self.country_code,
            "access_info": self.access_info,
            "participant_id_url": self.participant_id_url,
            "profile": self.profile_dict(),
        }

    def export_profiles(self) -> QuerySet[Result]:
        """Export participant profile result objects

        Returns:
            All profile results from a participant

        Example:
            Print all the questions and answers from a participant's profile results
            ```python
            all_profile_results = participant.export_profiles()
            for profile in all_profile_results:
                print(f"{profile.question_key} - {profile.given_response}")
            ```
        """

        return self.result_set.all()

    def profile(self) -> QuerySet[Result]:
        """Get all the answered profile results of this participant

        Returns:
            All answered profile results from a participant

        Example:
            Print all the questions and answers from a participant's profile results
            ```python
            all_profile_results = participant.profile()
            for profile in all_profile_results:
                print(f"{profile.question_key} - {profile.given_response}")
            ```
        """
        return self.result_set.all().filter(given_response__isnull=False)

    def profile_dict(self) -> dict:
        """Get full profile data in one object

        Returns:
            All profile data from a Participant in one object

        Example:
            Print all the questions, answers and scores from a participant's profile results
            ```python
            all_profile_results = participant.profile_dict()
            for key, value in all_profile_results:
                print(f"{key} - {value}")
            ```
        """
        profile_dict = {}
        for profile in self.profile():
            profile_dict[profile.question_key] = profile.given_response
            if profile.score:
                profile_dict[f'{profile.question_key}_score'] = profile.score
        return profile_dict

    def is_dutch(self) -> bool:
        """Return if a participant is tagged with the country code of the Netherlands (nl)

        Returns:
            Wether a participant is located in the Netherlands or not.

        Example:
            Check if the participant is from the netherlands.
            ```python
            if participant.is_dutch():
                # block of code to be executed if the condition is true
            ```
        """
        return self.country_code == "nl"

    def scores_per_experiment(self) -> list[dict]:
        """Scores per finished experiment session

        Returns:
            All finished sessions and best scores from a Participant

        Example:
            Print score per experiment
            ```python
            scores_list = participant.scores_per_experiment()
            for scores_object in scores_list:
                for key, value in scores_object:
                    print(f"{key} - {value}")
            ```
        """
        scores = []

        # Get all finished sessions
        sessions = self.session_set.exclude(
            finished_at=None).order_by('-final_score')

        hits = {}

        # Create best rank/score data per experiment session
        for session in sessions:

            if session.block.slug in hits:
                continue

            hits[session.block.slug] = True

            scores.append(
                {
                    "block_slug": session.block.slug,
                    "rank": session.block.get_rules().rank(session),
                    "score": session.final_score,
                    "date": naturalday(session.finished_at),
                }
            )

        return scores

    def score_sum(self, question_group_key:str) -> float:
        """ Sums scores of all profile results with questions in a question group

        Args:
            question_group_key: from `question.models.QuestionGroup.key`

        Returns:
            Total score of all profile results from a Participant

        Example:
            Get the total score of all participant's profile results from a specific question group
            ```python
            score_sum = participant.score_sum()
            ```
        """

        question_keys = QuestionGroup.objects.get(key=question_group_key).questions.values_list("key", flat=True)

        return self.result_set.all().filter(question_key__in=question_keys).aggregate(Sum("score"))['score__sum']
