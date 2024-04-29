# Generated by Django 3.2.25 on 2024-03-25 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0027_experimentseriesgroup_groupedexperiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentseries',
            name='about_content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='experimentseriesgroup',
            name='order',
            field=models.IntegerField(default=0, help_text='Order of the group in the series. Lower numbers come first.'),
        ),
        migrations.AlterField(
            model_name='experimentseriesgroup',
            name='randomize',
            field=models.BooleanField(default=False, help_text='Randomize the order of the experiments in this group.'),
        ),
        migrations.AlterField(
            model_name='groupedexperiment',
            name='order',
            field=models.IntegerField(default=0, help_text='Order of the experiment in the group. Lower numbers come first.'),
        ),
    ]
