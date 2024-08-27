from pathlib import Path

from django.db import migrations
from django.core.files.base import File

from experiment.models import Block, Experiment, ExperimentTranslatedContent, Phase

def add_experiment_and_phase(apps, schema_editor):
    blocks = Block.objects.all()
    for block in blocks:
        if block.phase is None:
            experiment = Experiment.objects.create(slug=block.slug)
            content = ExperimentTranslatedContent.objects.create(
                        experiment=experiment,
                        name=block.name
                    )
            rules = block.get_rules()
            try:
                consent_path = Path(rules.default_consent_file)
                with consent_path.open(mode='rb') as f:
                    content.consent = File(f, name=consent_path.name)
                    content.save()
            except:
                pass
            phase = Phase.objects.create(name=f'{block.name}_phase', series=experiment)
            block.phase = phase
            block.save()

def remove_experiment_and_phase(apps, schema_editor):
    blocks = Block.objects.all()
    for block in blocks:
        if block.phase and block.phase.name == f'{block.name}_phase':
            phase = Phase.objects.get(block.phase)
            Experiment.objects.delete(phase.series)
            block.phase = None
            block.save()
            phase.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0052_remove_experiment_first_experiments_and_more'),
    ]

    operations = [
        migrations.RunPython(add_experiment_and_phase, remove_experiment_and_phase),
    ]
