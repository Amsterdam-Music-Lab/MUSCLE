from django.db import models
from django.utils import timezone

from result.models import Result


class Session(models.Model):
    """Experiment session by a participant"""

    block = models.ForeignKey("experiment.Block", on_delete=models.CASCADE, blank=True, null=True)
    participant = models.ForeignKey("participant.Participant", on_delete=models.CASCADE)
    playlist = models.ForeignKey("section.Playlist", on_delete=models.SET_NULL, blank=True, null=True)

    started_at = models.DateTimeField(db_index=True, default=timezone.now)
    finished_at = models.DateTimeField(db_index=True, default=None, null=True, blank=True)
    json_data = models.JSONField(default=dict, blank=True, null=True)
    final_score = models.FloatField(db_index=True, default=0.0)
    current_round = models.IntegerField(default=1)

    def __str__(self):
        return "Session {}".format(self.id)

    def result_count(self):
        """Number of results"""
        return self.result_set.count()

    result_count.short_description = "Results"

    def total_score(self):
        """Sum of all result scores"""
        score = self.result_set.aggregate(models.Sum("score"))
        return self.block.bonus_points + (score["score__sum"] if score["score__sum"] else 0)

    def last_score(self):
        """Get last score, or return 0 if no scores are set"""

        if self.result_set.count() > 0:
            return self.result_set.last().score

        return 0

    def last_result(self):
        """Get last result"""
        result = self.result_set.last()

        return Result.objects.get(pk=result.id)

    def last_song(self):
        """Return artist and name of previous song,
        or return empty string if no scores are set
        """
        section = self.previous_section()
        if section:
            return "{} - {}".format(section.song.artist, section.song.name)
        return ""

    def previous_section(self):
        """Get previous song presented in an experiment"""
        valid_results = self.result_set.filter(score__isnull=False)
        if valid_results.count() > 0:
            result = valid_results.last()
            if result.section:
                return result.section
        return None

    def save_json_data(self, data):
        """Merge data with json_data, overwriting duplicate keys."""
        new_data = self.load_json_data()
        new_data.update(data)
        self.json_data = new_data
        self.save()

    def load_json_data(self):
        """Get json data as object"""
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

    def export_results(self):
        # export session result objects
        return self.result_set.all()

    def is_finished(self):
        """Determine if the session is finished"""
        return self.finished_at

    def rounds_complete(self):
        """Determine if there are results for each experiment round"""
        return self.get_rounds_passed() >= self.block.rounds

    def get_rounds_passed(self, counted_result_keys: list = []):
        """Get number of rounds passed, measured by the number of results on this session,
        taking into account the `counted_result_keys` array that may be defined per rules file
        - params:
            exclude_irrelevant: specify if question_keys which are not in the
            `counted_result_keys` array of the rules file should be counted
        """
        results = self.result_set
        if counted_result_keys:
            results = results.filter(question_key__in=counted_result_keys)
        return results.count()

    def get_used_song_ids(self, exclude={}):
        """Get a list of song ids from the sections of this session's results"""
        return (res.section.song.id for res in self.result_set.exclude(**exclude).filter(section__isnull=False))

    def get_unused_song_ids(self, filter_by={}):
        """Get a list of unused song ids from this session's playlist"""
        # Get all song ids from the current playlist
        song_ids = (
            self.playlist.section_set.filter(**filter_by).order_by("song").values_list("song_id", flat=True).distinct()
        )
        # Get all song ids from results
        used_song_ids = self.get_used_song_ids()
        return list(set(song_ids) - set(used_song_ids))

    def block_rules(self):
        """Get rules class to be used for this session"""
        return self.block.get_rules()

    def finish(self):
        """Finish current session"""
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
