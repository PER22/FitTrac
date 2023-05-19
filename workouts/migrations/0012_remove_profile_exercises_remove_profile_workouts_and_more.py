# Generated by Django 4.2.1 on 2023-05-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0011_remove_workout_user_alter_profile_exercises_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='workouts',
        ),
        migrations.AddField(
            model_name='profile',
            name='exercises',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='workouts.exercise'),
        ),
        migrations.AddField(
            model_name='profile',
            name='workouts',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='workouts.workout'),
        ),
    ]
