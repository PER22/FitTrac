from django.contrib import admin
from .models import Workout, Exercise, Profile, Set, WorkoutExercise, ProfileWorkout

# Register your models here.
admin.site.register(Set)
admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(WorkoutExercise)
admin.site.register(ProfileWorkout)
