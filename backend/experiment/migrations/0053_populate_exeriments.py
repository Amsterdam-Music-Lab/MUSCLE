from pathlib import Path

from django.db import migrations
from django.core.files.base import File

from experiment.models import Block, Experiment, ExperimentTranslatedContent, Phase

def add_experiment_and_phase(apps, schema_editor):
    blocks = Block.objects.all()
    for block in blocks:
        if block.phase is None:
            experiment = Experiment.objects.create(slug=block.slug)
            rules = block.get_rules()
            consent_path = Path(rules.default_consent_file)
            if consent_path:
                with consent_path.open(mode='rb') as f:
                    ExperimentTranslatedContent.objects.create(
                        experiment=experiment,
                        consent=File(f, name=consent_path.name)
                    )
            phase = Phase.objects.create(name=f'{block.name}_phase', series=experiment)
            block.phase = phase
            block.save()


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0052_remove_experiment_first_experiments_and_more'),
    ]

    operations = [
        migrations.RunPython(add_experiment_and_phase)
    ]
