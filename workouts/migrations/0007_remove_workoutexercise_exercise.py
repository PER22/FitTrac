# Generated by Django 4.2.1 on 2023-05-16 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0006_profile_bio_alter_profile_exercises_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutexercise',
            name='exercise',
        ),
    ]
