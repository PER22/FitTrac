from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

WORKOUT_GEAR = (
    ("N", "no equipment"),
    ("M", "a machine"),
    ("B", "barbells"),
    ("Y", "yoga equipment"),
    ("D", "dumbells"),
    ("R", "resistance bands"),
    ("T", "TRX bands"),
)


TRAINING_TYPES = (
    ("U", "unspecified"),
    ("W", "warmup"),
    ("Y", "yoga"),
    ("S", "stretching"),
    ("A", "agility"),
    ("F", "strength"),
    ("R", "rehabilitation"),
    ("C", "cardio"),
)


class Exercise(models.Model):
    name = models.CharField(max_length=50, default="Unnamed Exercise")
    equipment = models.CharField(
        max_length=1, choices=WORKOUT_GEAR, default=WORKOUT_GEAR[0][0]
    )
    type = models.CharField(
        max_length=1, choices=TRAINING_TYPES, default=TRAINING_TYPES[0][0]
    )
    description = models.TextField(max_length=250, default="No description provided")
    def __str__(self):
        builtString = self.name
        if self.equipment:
            builtString += f" with {self.get_equipment_display()}"
        if self.equipment:
            builtString += f" as a {self.get_type_display()} exercise"
        if self.description:
            builtString += f": {self.description}"
        else:
            builtString += f"."           
        return builtString
    def get_absolute_url(self):
        return reverse('exercise_detail', kwargs={'exercise_pk': self.pk})

class Workout(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=250, default="")
    difficulty_rating = models.IntegerField(
        default=5, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_absolute_url(self):
        return reverse("workout_detail", kwargs={"workout_pk": self.id})


class Set(models.Model):
    workout = models.ForeignKey(
        "Workout", on_delete=models.CASCADE, related_name="sets"
    )
    exercise = models.ForeignKey(
        "Exercise", on_delete=models.CASCADE, related_name="sets"
    )
    duration = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    resistance = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    time = models.FloatField(null=True, blank=True)
    reps = models.FloatField(null=True, blank=True)

    def clean(self):
        super().clean()
        if not any(
            [
                self.duration,
                self.weight,
                self.resistance,
                self.distance,
                self.time,
                self.reps,
            ]
        ):
            raise ValidationError(
                "At least one attribute (duration, weight, resistance, distance, time, reps) must be non-null"
            )
            
    def __str__(self):
        return f"Finally, a Set"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic_url = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    workouts = models.ManyToManyField("Workout", related_name="profile", blank=True)
    exercises = models.ManyToManyField("Exercise", related_name="profile", blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'profile_pk': self.pk})


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sets = models.ManyToManyField(Set, blank=True)
    rest_time = models.IntegerField(default=60)
    notes = models.TextField(max_length=250, default="")
    
    def __str__(self):
        return f"Sets in ({self.workout})"


class ProfileWorkout(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('profile', 'workout')