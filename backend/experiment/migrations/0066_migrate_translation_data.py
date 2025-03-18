# Generated by Django 4.2.18 on 2025-03-17 11:14

from django.db import migrations


class Migration(migrations.Migration):

    def populate_block_translations(apps, schema_editor):
        Block = apps.get_model('experiment', 'Block')
        BlockTranslatedContent = apps.get_model('experiment', 'BlockTranslatedContent')
        for block in Block.objects.all():
            btcs = BlockTranslatedContent.objects.filter(block=block)
            new_translation_object = BlockTranslatedContent.objects.create(
                block=block, language='cy'
            )  # set fake language for now
            for btc in btcs.all():
                if btc.language in ['en', 'nl', 'pt']:
                    setattr(new_translation_object, f'name_{btc.language}', btc.name)
                    setattr(new_translation_object, f'description_{btc.language}', btc.description)
                elif btc.language == 'zh':
                    setattr(new_translation_object, 'name_zh_hans', btc.name)
                    setattr(
                        new_translation_object, 'description_zh_hans', btc.description
                    )
                new_translation_object.save()

    def remove_block_translations(apps, schema_editor):
        BlockTranslatedContent = apps.get_model('experiment', 'BlockTranslatedContent')
        BlockTranslatedContent.objects.filter(language='cy').delete()

    def populate_experiment_translations(apps, schema_editor):
        Experiment = apps.get_model('experiment', 'Experiment')
        ExperimentTranslatedContent = apps.get_model('experiment', 'ExperimentTranslatedContent')
        for exp in Experiment.objects.all():
            etcs = ExperimentTranslatedContent.objects.filter(experiment=exp)
            min_index = etcs.order_by('index').first().index
            new_translation_object = ExperimentTranslatedContent.objects.create(
                experiment=exp, language='cy'
            )  # set fake language
            for etc in etcs.all():
                lang_code = 'zh_hans' if etc.language == 'zh' else etc.language
                if not etc.name and etc.index == min_index:
                    new_translation_object.name = etc.name
                    new_translation_object.description = etc.description
                    new_translation_object.consent = etc.consent
                    new_translation_object.about_content = etc.about_content
                    new_translation_object.social_media_message = (
                        etc.social_media_message
                    )
                    new_translation_object.disclaimer = etc.disclaimer
                    new_translation_object.privacy = etc.privacy

                if etc.language in ['en', 'nl', 'pt', 'zh']:
                    setattr(new_translation_object, f'name_{lang_code}', etc.name)
                    setattr(
                        new_translation_object,
                        f'description_{lang_code}',
                        etc.description,
                    )
                    setattr(new_translation_object, f'consent_{lang_code}', etc.consent)
                    setattr(
                        new_translation_object,
                        f'about_content_{lang_code}',
                        etc.about_content,
                    )
                    setattr(
                        new_translation_object,
                        f'social_media_message_{lang_code}',
                        etc.social_media_message,
                    )
                    setattr(
                        new_translation_object,
                        f'disclaimer_{lang_code}',
                        etc.disclaimer,
                    )
                    setattr(new_translation_object, f'privacy_{lang_code}', etc.privacy)
                etc.index = 42  # set to an arbitray largish value
                etc.save()
                new_translation_object.save()

    def remove_experiment_translations(apps, schema_editor):
        ExperimentTranslatedContent = apps.get_model(
            'experiment', 'ExperimentTranslatedContent'
        )
        ExperimentTranslatedContent.objects.filter(language='cy').delete()

    dependencies = [
        ('experiment', '0065_add_modeltranslations'),
    ]

    operations = [
        migrations.RunPython(populate_block_translations, remove_block_translations),
        migrations.RunPython(
            populate_experiment_translations, remove_experiment_translations
        ),
    ]
