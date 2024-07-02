import random
from django.db import models
from django.utils import timezone

from section.models import Section


class Session(models.Model):
    """Experiment session by a participant"""

    experiment = models.ForeignKey('experiment.Experiment', on_delete=models.CASCADE, blank=True, null=True)
    participant = models.ForeignKey('participant.Participant', on_delete=models.CASCADE)
    playlist = models.ForeignKey('section.Playlist', on_delete=models.SET_NULL,
                                 blank=True, null=True)

    started_at = models.DateTimeField(db_index=True, default=timezone.now)
    finished_at = models.DateTimeField(
        db_index=True, default=None, null=True, blank=True)
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
            return "{} - {}".format(section.song.artist, section.song.name)
        return ""

    def previous_section(self):
        """ Get previous song presented in an experiment """
        valid_results = self.result_set.filter(score__isnull=False)
        if valid_results.count() > 0:
            result = valid_results.last()
            if result.section:
                return result.section
        return None

    def save_json_data(self, data):
        """Merge data with json_data, overwriting duplicate keys.
        """
        new_data = self.load_json_data()
        new_data.update(data)
        self.json_data = new_data
        self.save()

    def load_json_data(self):
        """Get json data as object"""
        return self.json_data if self.json_data else {}

    def export_admin(self):
        """Export data for admin"""
        return {
            'session_id': self.id,
            'participant': self.participant.id,
            'started_at': self.started_at.isoformat(),
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'json_data': self.load_json_data(),
            'results': [result.export_admin() for result in self.result_set.all()]
        }

    def export_results(self):
        # export session result objects
        return self.result_set.all()

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

    def get_current_round(self):
        return self.current_round

    def set_current_round(self, round_number):
        self.current_round = round_number
        self.save()

    def reset_rounds(self):
        self.current_round = 1
        self.save()

    def increment_round(self):
        self.current_round += 1
        self.save()

    def decrement_round(self):
        self.current_round -= 1
        self.save()

    def get_used_song_ids(self):
        """Get a list of song ids from the sections of this session's results"""
        return (res.section.song.id for res in self.result_set.filter(section__isnull=False))

    def get_unused_song_ids(self):
        """Get a list of unused song ids from this session's playlist"""
        # Get all song ids from the current playlist
        song_ids = self.playlist.get_available_song_ids()
        # Get all song ids from results
        used_song_ids = self.get_used_song_ids()
        return list(set(song_ids) - set(used_song_ids))

    def get_used_section(self, filter_by: dict = {}, exclude: dict = {}) -> Section:
        ''' get a section from the playlist which has been used previously in this session
        :param filter_by: a dictionary with which to filter by section fields
        :param exclude: a dictionary with which to exclude certain sections
        '''
        used_sections = [
            result.section.id for result in self.result_set.filter(section__isnull=False)]
        if not used_sections:
            raise Section.DoesNotExist
        sections = self.playlist.section_set.all().filter(
            pk__in=used_sections).exclude(**exclude).filter(**filter_by)
        if sections:
            return random.choice(sections)
        raise Section.DoesNotExist

    def get_unused_section(self, filter_by: dict = {}, exclude: dict = {}) -> Section:
        ''' get a section from the playlist which has not yet been used in this session
        :param filter_by: a dictionary with which to filter by section fields
        :param exclude: a dictionary with which to exclude certain sections
        '''
        used_sections = [
            result.section.id for result in self.result_set.filter(section__isnull=False)]
        if not used_sections:
            return self.get_random_section()
        else:
            sections = self.playlist.section_set.all().exclude(
                pk__in=used_sections).exclude(**exclude).filter(**filter_by)
            if sections:
                return random.choice(sections)
        raise Section.DoesNotExist

    def get_random_section(self, filter_by: dict = {}, exclude: dict = {}) -> Section:
        ''' return a section from the playlist randomly
        :param filter_by: a dictionary with which to filter by section fields
        :param exclude: a dictionary with which to exclude certain sections
        '''
        sections = self.playlist.section_set.all().exclude(**exclude).filter(**filter_by)
        if not sections:
            raise Section.DoesNotExist
        return random.choice(sections)

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

    def percentile_rank(self, exclude_unfinished):
        """Get session percentile rank based on final_score, within current experiment"""
        session_set = self.experiment.session_set
        if exclude_unfinished:
            session_set = session_set.filter(finished_at__isnull=False)
        n_session = session_set.count()
        if n_session == 0:
            return 0.0  # Should be impossible but avoids x/0
        n_lte = \
            session_set.filter(final_score__lte=self.final_score).count()
        n_eq = session_set.filter(final_score=self.final_score).count()
        return 100.0 * (n_lte - (0.5 * n_eq)) / n_session

    def question_bonus(self, bonus=100, skip_penalty=5):
        """Get the question bonus, given by the bonus reduced with number of skipped questions times the skip_penalty"""
        return bonus + self.skipped_questions() * skip_penalty

    def total_questions(self):
        """ Get total number of profile questions in this session """
        return self.result_count()

    def skipped_questions(self):
        """Get number of skipped (empty) profile questions for this session"""
        return self.result_set.filter(given_response="").count()

    def answered_questions(self):
        """Get number of answered (non-empty) profile questions for this session"""
        return self.result_set.exclude(given_response="").count()

    def get_relevant_results(self, question_keys=[]):
        results = self.result_set
        if question_keys:
            return results.filter(question_key__in=question_keys)
        return results

    def get_previous_result(self, question_keys=[]):
        results = self.get_relevant_results(question_keys)
        return results.order_by('-created_at').first()
