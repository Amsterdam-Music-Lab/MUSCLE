from django.db import models
from django.utils import timezone
from experiment.rules import EXPERIMENT_RULES
from experiment.rules.util.iso_languages import ISO_LANGUAGES
from . import Playlist

language_choices = [(key, ISO_LANGUAGES[key]) for key in ISO_LANGUAGES.keys()]
language_choices[0] = ('', 'Unset')

class Experiment(models.Model):
    """Root entity for configuring experiments"""

    playlists = models.ManyToManyField(Playlist)
    name = models.CharField(db_index=True, max_length=64)
    slug = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)
    rounds = models.PositiveIntegerField(default=10)
    bonus_points = models.PositiveIntegerField(default=0)
    rules = models.CharField(default="", max_length=64)
    language = models.CharField(
        default="", blank=True, choices=language_choices, max_length=2)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def session_count(self):
        """Number of sessions"""
        return self.session_set.count()

    session_count.short_description = "Sessions"

    def playlist_count(self):
        """Number of playlists"""
        return self.playlists.count()

    playlist_count.short_description = "Playlists"

    def current_participants(self):
        """Get distinct list of participants"""
        participants = {}
        for session in self.session_set.all():
            participants[session.participant.id] = session.participant

        return participants.values()

    def export_admin(self):
        """Export data for admin"""
        return {
            'exportedAt': timezone.now().isoformat(),
            'experiment': {
                'id': self.id,
                'name': self.name,
                'sessions': [session.export_admin() for session in self.session_set.all()],
                'participants': [
                    participant.export_admin() for participant in self.current_participants()
                ]
            },
        }
    
    def export_table(self):
        """Export tabular data for admin"""
        rows = [] # a list of dictionaries
        fieldnames = set() # keep track of all potential fieldnames
        for session in self.session_set.all():
            profile = session.participant.export_admin()
            session_finished = session.finished_at.isoformat() if session.finished_at else None
            for result in session.result_set.all():
                result_details = result.export_admin()['details']
                row = {
                    'experiment_id': self.id, 
                    'experiment_name': self.name,
                    'participant_id': profile['id'],
                    'participant_country': profile['country_code'],
                    'session_start': session.started_at.isoformat(),
                    'session_end': session_finished,
                    'result_created_at': result.created_at.isoformat(),
                    'result_score': result.score,
                    'experiment_view': result_details.pop('view', None)
                }
                row.update(profile['profile'])
                for key in result_details.keys():
                    row.update({'{}_{}'.format(key, detail_key): result_details[key][detail_key] for detail_key in result_details[key].keys()})
                rows.append(row)
                fieldnames.update(row.keys())
        return rows, list(fieldnames)

    def get_rules(self):
        """Get rules class to be used for this session"""
        return EXPERIMENT_RULES[self.rules]

    def max_score(self):
        """Get max score from all sessions with a positive score"""
        score = self.session_set.filter(
            final_score__gte=0).aggregate(models.Max('final_score'))
        if 'final_score__max' in score:
            return score['final_score__max']

        return 0
