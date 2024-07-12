# Generated by Django 4.2.11 on 2024-07-03 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('experiment', '0042_rename_experiment_to_block'), ('experiment', '0043_alter_groupedexperiment_options_and_more'), ('experiment', '0044_rename_groupedexperiment_groupedblock'), ('experiment', '0045_rename_experiment_feedback_block')]

    dependencies = [
        ('experiment', '0041_socialmediaconfig'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Experiment',
            new_name='Block',
        ),
        migrations.RenameField(
            model_name='groupedexperiment',
            old_name='experiment',
            new_name='block',
        ),
        migrations.AlterModelOptions(
            name='groupedexperiment',
            options={'ordering': ['index'], 'verbose_name_plural': 'Grouped Blocks'},
        ),
        migrations.RemoveField(
            model_name='groupedexperiment',
            name='order',
        ),
        migrations.AddField(
            model_name='groupedexperiment',
            name='index',
            field=models.IntegerField(default=0, help_text='Order of the block in the phase. Lower numbers come first.'),
        ),
        migrations.AlterField(
            model_name='block',
            name='url',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='URL with more information about the block'),
        ),
        migrations.AlterField(
            model_name='groupedexperiment',
            name='phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='experiment.phase'),
        ),
        migrations.RenameModel(
            old_name='GroupedExperiment',
            new_name='GroupedBlock',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='experiment',
            new_name='block',
        ),
    ]