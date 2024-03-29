# Generated by Django 3.2.16 on 2023-01-10 08:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participant', '0001_initial'),
        ('session', '0001_initial'),
        ('section', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('question_key', models.CharField(max_length=64, default='')),
                ('expected_response', models.CharField(blank=True, max_length=100, null=True)),
                ('given_response', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.CharField(default='', max_length=100)),
                ('score', models.FloatField(blank=True, null=True)),
                ('scoring_rule', models.CharField(default='', max_length=64)),
                ('json_data', models.TextField(blank=True)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='section.section')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, blank=True, null=True, to='session.session')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, blank=True, null=True, to='participant.participant'))
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
