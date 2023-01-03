import json
import random
from django.db import models
from django.utils import timezone

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist, Section
# from participant_profile.models import Profile


class Session(models.Model):
    """Experiment session by a participant"""

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL,
                                 blank=True, null=True)

    started_at = models.DateTimeField(db_index=True, default=timezone.now)
    finished_at = models.DateTimeField(
        db_index=True, default=None, null=True, blank=True)
    json_data = models.TextField(blank=True)
    final_score = models.FloatField(db_index=True, default=0.0)

    def __str__(self):
        return "Session {}".format(self.id)

    def result_count(self):
        """Number of results"""
        return self.result_set.count()

    result_count.short_description = "Results"

    def total_score(self):
        """Sum of all result scores"""
        score = self.result_set.aggregate(models.Sum('score'))
        return self.experiment.bonus_points + (score['score__sum'] if score['score__sum'] else 0)

    def last_score(self):
        """Get last score, or return 0 if no scores are set"""

        if self.result_set.count() > 0:
            return self.result_set.last().score

        return 0

    def last_result(self):
        """Get last result"""
        return self.result_set.last()

    def last_song(self):
        """Return artist and name of previous song, 
        or return empty string if no scores are set
        """

        section = self.previous_section()
        if section:
            return "{} - {}".format(section.artist, section.name)
        return ""

    def previous_section(self):
        """ Get previous song presented in an experiment """
        if self.result_set.count() > 0:
            result = self.result_set.last()
            if result.section:
                return result.section
        return None

    def save_json_data(self, data):
        """Convert json data object to string and store in json_data"""
        self.json_data = json.dumps(data, indent=4) if data else "{}"

    def merge_json_data(self, data):
        """Convert json data object to string and merge with json_data, overwriting duplicate keys.

        Only valid for JSON objects/Python dicts.
        """
        if data:
            self.json_data = json.dumps(
                {**self.load_json_data(), **data}, indent=4)

    def load_json_data(self):
        """Get json data object from string json_data"""
        return json.loads(self.json_data) if self.json_data else {}

    def export_admin(self):
        """Export data for admin"""
        return {
            'participant': self.participant.id,
            'started_at': self.started_at.isoformat(),
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'json_data': self.load_json_data(),
            'results': [result.export_admin() for result in self.result_set.all()]
        }

    def is_finished(self):
        """Determine if the session is finished"""
        return self.finished_at

    def rounds_complete(self):
        """Determine if there are results for each experiment round"""
        return self.rounds_passed() >= self.experiment.rounds

    def rounds_passed(self):
        """Get number of rounds passed"""
        return self.result_set.count()

    def get_next_round(self):
        """Get next round number"""
        return self.rounds_passed() + 1

    def song_ids(self):
        """Get a list of song ids from the sections of this session's results"""
        return list(map(
            lambda result: result.section.pk if result.section else None,
            self.result_set.filter(section__isnull=False)
        ))

    def section_from_any_song(self, filter_by={}):
        """Get a random section with a Dutch IP check.

        To ensure appropriate IP restrictions, most rules should this
        method instead of operating on the playlist directly.
        """

        # Get pks from sections with given filter and song_id
        pks = self.playlist.section_set.filter(
            # IP checking is overridable in filter_by.
            **(
                {}
                if self.participant.is_dutch()
                else {'restrict_to_nl': False}
            ),
            **filter_by
        ).values_list('pk', flat=True)

        # Return None if nothing matches
        if len(pks) == 0:
            return None

        # Return a random section
        return self.playlist.section_set.get(pk=random.choice(pks))

    def all_sections(self, filter_by={}):
        """Get all section with a Dutch IP check.

        To ensure appropriate IP restrictions, most rules should this
        method instead of operating on the playlist directly.
        """

        # Get pks from sections with given filter and song_id
        pks = self.playlist.section_set.filter(
            # IP checking is overridable in filter_by.
            **(
                {}
                if self.participant.is_dutch()
                else {'restrict_to_nl': False}
            ),
            **filter_by
        ).values_list('pk', flat=True)

        # Return None if nothing matches
        if len(pks) == 0:
            return None

        # Return all sections
        return self.playlist.section_set.all()

    def section_from_song(self, song_id, filter_by={}):
        """Get a random section from a particular song"""
        return self.section_from_any_song({**filter_by, 'pk': song_id})

    def unused_song_ids(self, filter_by={}):
        """Get a list of unused song ids from this session's playlist"""
        # Get all song ids from playlists
        song_ids = self.playlist.song_ids(filter_by)

        # Get all song ids from results
        used_song_ids = self.song_ids()

        return list(set(song_ids) - set(used_song_ids))

    def section_from_unused_song(self, filter_by={}):
        """Get a random section from any unused song"""

        song_ids = self.unused_song_ids(filter_by)

        if len(song_ids) == 0:
            return None

        # Get a random song_id
        song_id = random.choice(song_ids)

        # Return a random section
        return self.section_from_song(song_id, filter_by)

    def section_from_used_song(self):
        """Get a random section from any used song"""

        song_ids = self.song_ids()

        if len(song_ids) == 0:
            return None

        # Get a random song_id
        song_id = random.choice(song_ids)

        # Return a random section
        return self.section_from_song(song_id)

    def experiment_rules(self):
        """Get rules class to be used for this session"""
        return self.experiment.get_rules()

    def finish(self):
        """Finish current session"""
        self.finished_at = timezone.now()
        self.final_score = self.total_score()

    def rank(self):
        """Get session rank based on final_score, within current experiment"""
        return self.experiment.session_set.filter(final_score__gte=self.final_score).values('final_score').annotate(total=models.Count('final_score')).count()

    def percentile_rank(self):
        """Get session percentile rank based on final_score, within current experiment"""
        if self.is_finished():
            finished_set = \
                self.experiment.session_set.filter(finished_at__isnull=False)
            n_finished = finished_set.count()
            if n_finished == 0:
                return 0.0  # Should be impossible but avoids x/0
            n_lte = \
                finished_set.filter(final_score__lte=self.final_score).count()
            n_eq = finished_set.filter(final_score=self.final_score).count()
            return 100.0 * (n_lte - (0.5 * n_eq)) / n_finished
        else:
            return 0.0

    def question_bonus(self, bonus=100, skip_penalty=5):
        """Get the question bonus, given by the bonus reduced with number of skipped questions times the skip_penalty"""
        return bonus + self.skipped_questions() * skip_penalty

    # def total_questions(self):
    #     """ Get total number of profile questions in this session """
    #     try:
    #         return Profile.objects.filter(session_id=self.id).count()
    #     except Profile.DoesNotExist:
    #         return 0

    # def skipped_questions(self):
    #     """Get number of skipped (empty) profile questions for this session"""
    #     try:
    #         return Profile.objects.filter(session_id=self.id, answer="").count()

    #     except Profile.DoesNotExist:
    #         return 0

    # def answered_questions(self):
    #     """Get number of answered (non-empty) profile questions for this session"""
    #     try:
    #         return Profile.objects.filter(session_id=self.id).exclude(answer="").count()

    #     except Profile.DoesNotExist:
    #         return 0
