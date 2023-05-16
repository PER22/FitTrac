from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
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
        return builtString


class Workout(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=250, default="")
    difficulty_rating = models.IntegerField(
        default=5, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    # Changing this instance method
    # does not impact the database, therefore
    # no makemigrations is necessary
    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_absolute_url(self):
        return reverse("workout_detail", kwargs={"pk": self.id})


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic_url = models.CharField(max_length=200, null=True, blank=True)
    workouts = models.ManyToManyField("Workout", related_name="profiles", blank=True)
    exercises = models.ManyToManyField("Exercise", related_name="profiles", blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.ManyToManyField(Set, blank=True)
    rest_time = models.IntegerField(default=60)
    notes = models.TextField(max_length=250, default="")
    

    def add_set(request, workout_id, exercise_id):
        workout = get_object_or_404(Workout, pk=workout_id)
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        
        # create a ModelForm instance using 
        # the data that was submitted in the form
        form = SetForm(request.POST)
        
        # validate the form
        if form.is_valid():
            # We want a model instance, but
            # we can't save to the db yet
            # because we have not assigned the
            # workout and exercise FKs.
            new_set = form.save(commit=False)
            new_set.workoutexercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise)
            new_set.save()
            
        return redirect('workout_detail', pk=workout.pk)

    def __str__(self):
        return f"{self.exercise} ({self.workout})"


class ProfileWorkout(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('profile', 'workout')