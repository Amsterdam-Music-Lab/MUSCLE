# Generated by Django 4.2.11 on 2024-07-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0039_auto_20240625_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phase',
            options={'ordering': ['index']},
        ),
        migrations.RemoveField(
            model_name='phase',
            name='order',
        ),
        migrations.AddField(
            model_name='phase',
            name='index',
            field=models.IntegerField(default=0, help_text='Index of the phase in the series. Lower numbers come first.'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='randomize',
            field=models.BooleanField(default=False, help_text='Randomize the order of the experiments in this phase.'),
        ),
    ]
