from typing import Iterable, Union

from django.db import models
from django.utils import timezone

from result.models import Result
from section.models import Section

class Session(models.Model):
    """A model defining a session of an experiment block of a participant

    Attributes:
        block (models.ForeignKey): each session is tied to a block
        participant (models.ForeignKey): each session is tied to a participant
        playlist (models.ForeignKey): most sessions will also be tied to a playlist
        started_at (datetime): a timestamp when a session is created, auto-populated
        finished_at (datetime): a timestamp of when `session.finish()` was called
        json_data (json): a field to keep track of progress through a blocks' rules in a session
        final_score: the final score of the session, usually the sum of all `Result` objects on the session
    """
    block = models.ForeignKey("experiment.Block", on_delete=models.CASCADE, blank=True, null=True)
    participant = models.ForeignKey("participant.Participant", on_delete=models.CASCADE)
    playlist = models.ForeignKey("section.Playlist", on_delete=models.SET_NULL, blank=True, null=True)

    started_at = models.DateTimeField(db_index=True, default=timezone.now)
    finished_at = models.DateTimeField(db_index=True, default=None, null=True, blank=True)
    json_data = models.JSONField(default=dict, blank=True, null=True)
    final_score = models.FloatField(db_index=True, default=0.0)

    def __str__(self):
        return "Session {}".format(self.id)

    def result_count(self) -> int:
        """
        Returns:
            number of results for this session
        """
        return self.result_set.count()

    result_count.short_description = "Results"

    def total_score(self) -> float:
        """
        Returns:
            sum of all result scores
        """
        score = self.result_set.aggregate(models.Sum("score"))
        return self.block.bonus_points + (score["score__sum"] if score["score__sum"] else 0)

    def last_score(self) -> float:
        """
        Returns:
            score of last result, or return 0 if there are no results yet
        """

        if self.result_set.count() > 0:
            return self.result_set.last().score

        return 0

    def last_result(self) -> Result:
        """
        Returns:
            last Result object
        """
        result = self.result_set.last()
        # retrieve updated Result object from database
        return Result.objects.get(pk=result.id)

    def last_song(self) -> str:
        """
        Returns:
            artist and name of section tied to previous result, if available, or an empty string
        """
        section = self.previous_section()
        if section:
            return section.song_label()
        return ""

    def previous_section(self) -> Union[Section, None]:
        """
        Returns:
            Section tied to previous result, if that result has a score and section, else None
        """
        valid_results = self.result_set.filter(score__isnull=False)
        if valid_results.count() > 0:
            result = valid_results.last()
            if result.section:
                return result.section
        return None

    def save_json_data(self, data: dict):
        """Merge data with json_data, overwriting duplicate keys.

        Attributes:
            data: a dictionary of data to save to the `json_data` field
        """
        new_data = self.load_json_data()
        new_data.update(data)
        self.json_data = new_data
        self.save()

    def load_json_data(self) -> dict:
        """
        Returns:
            json data as object
        """
        return self.json_data if self.json_data else {}

    def _export_admin(self):
        """Export data for admin"""
        return {
            "session_id": self.id,
            "participant": self.participant.id,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "json_data": self.load_json_data(),
            "results": [result._export_admin() for result in self.result_set.all()],
        }

    def _export_results(self):
        # export session result objects
        return self.result_set.all()

    def _is_finished(self) -> bool:
        """Determine if the session is finished"""
        return self.finished_at

    def rounds_complete(self) -> bool:
        """
        Returns:
            True if there are results for each experiment round
        """
        return self.get_rounds_passed() >= self.block.rounds

    def get_rounds_passed(self, counted_result_keys: list = []) -> int:
        """Get number of rounds passed, measured by the number of results on this session,
        taking into account the `counted_result_keys` array that may be defined per rules file

        Attributes:
            counted_result_keys: array of the Result.key strings whish should be taken into account for counting rounds; if empty, all results will be counted.

        Returns:
            number of results, filtered by `counted_result_keys`, if supplied
        """
        results = self.result_set
        if counted_result_keys:
            results = results.filter(question_key__in=counted_result_keys)
        return results.count()

    def get_used_song_ids(self, exclude: dict = {}) -> Iterable[int]:
        """Get a list of song ids already used in this session

        Attributes:
            exclude: a dictionary by which to exclude specific results in this session, using [Django's querying syntax](https://docs.djangoproject.com/en/4.2/topics/db/queries/)

        Returns:
            a list of song ids from the sections of this session's results
        """
        return (res.section.song.id for res in self.result_set.exclude(**exclude).filter(section__isnull=False))

    def get_unused_song_ids(self, filter_by: dict = {}) -> Iterable[int]:
        """Get a list of unused song ids from this session's playlist

        Attributes:
            filter_by: a dictionary by which to select sections from the playlist (e.g., a certain tag), using [Django's querying syntax](https://docs.djangoproject.com/en/4.2/topics/db/queries/)

        Returns:
            a list of song ids which haven't been used in this session yet
        """
        # Get all song ids from the current playlist
        song_ids = (
            self.playlist.section_set.filter(**filter_by).order_by("song").values_list("song_id", flat=True).distinct()
        )
        # Get all song ids from results
        used_song_ids = self.get_used_song_ids()
        return list(set(song_ids) - set(used_song_ids))

    def block_rules(self):
        """
        Returns:
            rules class to be used for this session
        """
        return self.block.get_rules()

    def finish(self):
        """Finish current session with the following steps:
        - set the `finished_at` timestamp to the current moment
        - set the `final_score` field to the sum of all results' scores
        """
        self.finished_at = timezone.now()
        self.final_score = self.total_score()

    def rank(self) -> int:
        """Get session rank based on final_score, within current experiment"""
        return (
            self.block.session_set.filter(final_score__gte=self.final_score)
            .values("final_score")
            .annotate(total=models.Count("final_score"))
            .count()
        )

    def percentile_rank(self, exclude_unfinished: bool) -> float:
        """Get session percentile rank based on final_score, within current experiment"""
        session_set = self.block.session_set
        if exclude_unfinished:
            session_set = session_set.filter(finished_at__isnull=False)
        n_session = session_set.count()
        if n_session == 0:
            return 0.0  # Should be impossible but avoids x/0
        n_lte = session_set.filter(final_score__lte=self.final_score).count()
        n_eq = session_set.filter(final_score=self.final_score).count()
        return 100.0 * (n_lte - (0.5 * n_eq)) / n_session

    def get_previous_result(self, question_keys: list = []) -> Result:
        results = self.result_set
        if question_keys:
            results = results.filter(question_key__in=question_keys)
        return results.order_by("-created_at").first()
