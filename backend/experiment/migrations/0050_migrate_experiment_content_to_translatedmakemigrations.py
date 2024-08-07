# Generated by Django 4.2.14 on 2024-07-31 13:41

from django.db import migrations


def migrate_experiment_content(apps, schema_editor):
    Experiment = apps.get_model("experiment", "Experiment")
    ExperimentTranslatedContent = apps.get_model("experiment", "ExperimentTranslatedContent")

    for experiment in Experiment.objects.all():
        ExperimentTranslatedContent.objects.create(
            experiment=experiment,
            index=0,
            language="en",  # Set English as default language
            name=experiment.name,
            description=experiment.description,
            consent=experiment.consent,
            about_content=experiment.about_content,
        )


def reverse_migrate_experiment_content(apps, schema_editor):
    Experiment = apps.get_model("experiment", "Experiment")
    ExperimentTranslatedContent = apps.get_model("experiment", "ExperimentTranslatedContent")

    for experiment in Experiment.objects.all():
        # find the English translation or the first one (lowest index)
        experiment_translations = ExperimentTranslatedContent.objects.filter(experiment=experiment)
        primary_translation = experiment_translations.order_by("index").first()

        if not primary_translation:
            continue

        experiment.name = primary_translation.name
        experiment.description = primary_translation.description
        experiment.consent = primary_translation.consent
        experiment.about_content = primary_translation.about_content
        experiment.save()

    ExperimentTranslatedContent.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("experiment", "0049_experimenttranslatedcontent"),
    ]

    operations = [
        migrations.RunPython(migrate_experiment_content, reverse_migrate_experiment_content),
    ]
