# Generated by Django 4.2.1 on 2023-05-18 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0009_exercise_user_workout_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='user',
        ),
    ]