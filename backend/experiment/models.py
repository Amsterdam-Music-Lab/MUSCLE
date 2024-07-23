import copy

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from typing import List, Dict, Tuple, Any
from experiment.standards.iso_languages import ISO_LANGUAGES
from theme.models import ThemeConfig
from image.models import Image
from session.models import Session
from typing import Optional

from .validators import markdown_html_validator, block_slug_validator

language_choices = [(key, ISO_LANGUAGES[key]) for key in ISO_LANGUAGES.keys()]
language_choices[0] = ('', 'Unset')


def consent_upload_path(instance, filename):
    """Generate path to save consent file based on block.slug"""
    folder_name = instance.slug
    return f'consent/{folder_name}/{filename}'


class Experiment(models.Model):
    """ A model to allow nesting multiple phases with blocks into a 'parent' experiment """
    name = models.CharField(max_length=64, default='')
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(max_length=64, default='')
    consent = models.FileField(upload_to=consent_upload_path,
                               blank=True,
                               default='',
                               validators=[markdown_html_validator()])
    theme_config = models.ForeignKey(
        "theme.ThemeConfig", blank=True, null=True, on_delete=models.SET_NULL)
    # first experiments in a test series, in fixed order
    first_experiments = models.JSONField(blank=True, null=True, default=dict)
    random_experiments = models.JSONField(blank=True, null=True, default=dict)
    # last experiments in a test series, in fixed order
    last_experiments = models.JSONField(blank=True, null=True, default=dict)
    # present random_experiments as dashboard
    dashboard = models.BooleanField(default=False)
    about_content = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)
    social_media_config: Optional['SocialMediaConfig']
    phases: models.QuerySet['Phase']

    def __str__(self):
        return self.name or self.slug

    class Meta:
        verbose_name_plural = "Experiments"

    def associated_blocks(self):
        phases = self.phases.all()
        return [
            experiment.block for phase in phases for experiment in list(phase.blocks.all())]

    def export_sessions(self):
        """export sessions for this experiment"""
        all_sessions = Session.objects.none()
        for block in self.associated_blocks():
            all_sessions |= Session.objects.filter(block=block).order_by('-started_at')
        return all_sessions

    def current_participants(self):
        """Get distinct list of participants"""
        participants = {}
        for session in self.export_sessions():
            participants[session.participant.id] = session.participant
        return participants.values()


class Phase(models.Model):
    name = models.CharField(max_length=64, blank=True, default='')
    series = models.ForeignKey(Experiment,
                               on_delete=models.CASCADE, related_name='phases')
    index = models.IntegerField(default=0, help_text='Index of the phase in the series. Lower numbers come first.')
    dashboard = models.BooleanField(default=False)
    randomize = models.BooleanField(
        default=False, help_text='Randomize the order of the experiments in this phase.')

    def __str__(self):
        compound_name = self.name or self.series.name or self.series.slug or 'Unnamed phase'

        if not self.name:
            return f'{compound_name} ({self.index})'

        return f'{compound_name}'

    class Meta:
        ordering = ['index']


class GroupedBlock(models.Model):
    block = models.ForeignKey('Block', on_delete=models.CASCADE)
    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
        related_name='blocks'
    )
    index = models.IntegerField(default=0, help_text='Order of the block in the phase. Lower numbers come first.')

    def __str__(self):
        return f'{self.block.name} - {self.phase.name} - {self.index}'

    class Meta:
        ordering = ['index']
        verbose_name_plural = "Grouped Blocks"


class Block(models.Model):
    """Root entity for configuring experiment blocks"""

    playlists = models.ManyToManyField('section.Playlist', blank=True)
    name = models.CharField(db_index=True, max_length=64)
    description = models.TextField(blank=True, default='')
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    slug = models.SlugField(db_index=True, max_length=64, unique=True, validators=[block_slug_validator])
    url = models.CharField(verbose_name='URL with more information about the block', max_length=100, blank=True, default='')
    hashtag = models.CharField(verbose_name='hashtag for social media', max_length=20, blank=True, default='')
    active = models.BooleanField(default=True)
    rounds = models.PositiveIntegerField(default=10)
    bonus_points = models.PositiveIntegerField(default=0)
    rules = models.CharField(default="", max_length=64)
    language = models.CharField(
        default="", blank=True, choices=language_choices, max_length=2)
    theme_config = models.ForeignKey(
        ThemeConfig,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    consent = models.FileField(upload_to=consent_upload_path,
                               blank=True,
                               default='',
                               validators=[markdown_html_validator()])

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
            'block': {
                'id': self.id,
                'name': self.name,
                'sessions': [session.export_admin() for session in self.session_set.all()],
                'participants': [
                    participant.export_admin() for participant in self.current_participants()
                ]
            },
        }

    def export_sessions(self):
        # export session objects
        return self.session_set.all()

    def export_table(self, session_keys: List[str], result_keys: List[str], export_options: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Export filtered tabular data for admin
            session_keys : session fieldnames to be included
            result_keys : result fieldnames to be included
            export_options : export options (see admin/forms.py)
        """
        rows = []  # a list of dictionaries
        fieldnames = set()  # keep track of all potential fieldnames
        result_prefix = ''
        for session in self.session_set.all():
            profile = session.participant.export_admin()
            session_finished = session.finished_at.isoformat() if session.finished_at else None
            # Get data for all potential session fields
            full_row = {
                'block_id': self.id,
                'block_name': self.name,
                'participant_id': profile['id'],
                'participant_country': profile['country_code'],
                'participant_access_info': profile['access_info'],
                'session_start': session.started_at.isoformat(),
                'session_end': session_finished,
                'final_score': session.final_score
            }
            row = {}
            # Add the selected sessions fields
            for session_key in session_keys:
                row[session_key] = full_row[session_key]
            # Add profile data if selected
            if 'export_profile' in export_options:
                row.update(profile['profile'])
            # Add session data
            if session.json_data != '':
                if 'session_data' in export_options:
                    # Convert json session data to csv columns if selected
                    if 'convert_session_json' in export_options:
                        row.update(session.load_json_data())
                    else:
                        row['session_data'] = session.load_json_data()
            fieldnames.update(row.keys())
            if session.result_set.count() == 0:
                # some sessions may have only profile questions
                rows.append(row)
            else:
                result_counter = 1
                # Create new row for each result
                if 'wide_format' in export_options:
                    this_row = copy.deepcopy(row)
                for result in session.result_set.all():
                    # Add all results to one row
                    if 'wide_format' not in export_options:
                        this_row = copy.deepcopy(row)
                    # Get data for al potential result fields
                    full_result_data = {
                        'section_name': result.section.song.name if result.section else None,
                        'result_created_at': result.created_at.isoformat(),
                        'result_score': result.score,
                        'result_comment': result.comment,
                        'expected_response': result.expected_response,
                        'given_response': result.given_response,
                        'question_key': result.question_key,
                    }

                    result_data = {}
                    # Add counter for single row / wide format
                    if 'wide_format' in export_options:
                        result_prefix = str(result_counter).zfill(3) + '-'
                        # add the selected result fields
                        for result_key in result_keys:
                            result_data[(result_prefix + result_key)
                                        ] = full_result_data[result_key]
                    else:
                        # add the selected result fields
                        for result_key in result_keys:
                            result_data[result_key] = full_result_data[result_key]
                    # Add result data
                    if result.json_data != '':
                        # convert result json data to csv columns if selected
                        if 'convert_result_json' in export_options:
                            if 'decision_time' in export_options:
                                result_data[result_prefix + 'decision_time'] = result.load_json_data().get(
                                    'decision_time', '')
                            if 'result_config' in export_options:
                                result_data[result_prefix + 'result_config'] = result.load_json_data().get(
                                    'config', '')
                        else:
                            if 'result_config' in export_options:
                                result_data[result_prefix +
                                            'result_data'] = result.load_json_data()
                    this_row.update(result_data)
                    fieldnames.update(result_data.keys())
                    result_counter += 1
                    # Append row for long format
                    if 'wide_format' not in export_options:
                        rows.append(this_row)
                # Append row for wide format
                if 'wide_format' in export_options:
                    rows.append(this_row)
        return rows, list(fieldnames)

    def get_rules(self):
        """Get instance of rules class to be used for this session"""
        from experiment.rules import BLOCK_RULES

        if self.rules not in BLOCK_RULES:
            raise ValueError(f"Rules do not exist (anymore): {self.rules} for block {self.name} ({self.slug})")

        cl = BLOCK_RULES[self.rules]
        return cl()

    def max_score(self):
        """Get max score from all sessions with a positive score"""
        score = self.session_set.filter(
            final_score__gte=0).aggregate(models.Max('final_score'))
        if 'final_score__max' in score:
            return score['final_score__max']

        return 0

    def add_default_question_series(self):
        """ Add default question_series to block"""
        from experiment.rules import BLOCK_RULES
        from question.models import Question, QuestionSeries, QuestionInSeries
        question_series = getattr(BLOCK_RULES[self.rules](), "question_series", None)
        if question_series:
            for i, question_series in enumerate(question_series):
                qs = QuestionSeries.objects.create(
                    name=question_series['name'],
                    block=self,
                    index=i+1,
                    randomize=question_series['randomize'])
                for i, question in enumerate(question_series['keys']):
                    QuestionInSeries.objects.create(
                        question_series=qs,
                        question=Question.objects.get(pk=question),
                        index=i+1)


class Feedback(models.Model):
    text = models.TextField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE)


class SocialMediaConfig(models.Model):
    experiment = models.OneToOneField(
        Experiment,
        on_delete=models.CASCADE,
        related_name='social_media_config'
    )

    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text=_("List of tags for social media sharing")
    )

    url = models.URLField(
        blank=True,
        help_text=_("URL to be shared on social media. If empty, the experiment URL will be used.")
    )

    content = models.TextField(
        blank=True,
        help_text=_("Content for social media sharing. Use {points} and {block_name} as placeholders."),
        default="I scored {points} points in {block_name}!"
    )

    SOCIAL_MEDIA_CHANNELS = [
        ('facebook', _('Facebook')),
        ('whatsapp', _('WhatsApp')),
        ('twitter', _('Twitter')),
        ('weibo', _('Weibo')),
        ('share', _('Share')),
        ('clipboard', _('Clipboard')),
    ]
    channels = ArrayField(
        models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHANNELS),
        blank=True,
        default=list,
        help_text=_("Selected social media channels for sharing")
    )

    def get_content(
            self, score: int | None = None, block_name: str | None = None
            ) -> str:
        if self.content:
            return self.content

        if not score or not block_name:
            raise ValueError("score and block_name are required")

        return _("I scored {points} points in {block_name}").format(
            score=score,
            block_name=block_name
        )

    def __str__(self):
        return f"Social Media for {self.experiment.name}"
