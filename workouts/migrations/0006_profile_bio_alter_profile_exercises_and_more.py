# Generated by Django 4.2.1 on 2023-05-16 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0005_profileworkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='exercises',
            field=models.ManyToManyField(blank=True, related_name='profile', to='workouts.exercise'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='workouts',
            field=models.ManyToManyField(blank=True, related_name='profile', to='workouts.workout'),
        ),
    ]
