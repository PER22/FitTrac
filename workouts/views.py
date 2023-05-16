import os
import uuid
import boto3
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Workout, Exercise, Set, Profile, User, WorkoutExercise, ProfileWorkout
from .forms import ExerciseForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
  
  
class WorkoutList(LoginRequiredMixin, ListView):
  model = Workout
  context_object_name = 'workouts'

class WorkoutDetail(LoginRequiredMixin, DetailView):
  model = Workout
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    exercise_form = ExerciseForm()
    context["exercise_form"] = exercise_form
    return context
  
  def add_set(request, workout_id, exercise_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    form = SetForm(request.POST)
    if form.is_valid():
      new_set = form.save(commit=False)
      new_set.workoutexercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise)
      new_set.save()
      
    return redirect('workout_detail', pk=workout.pk)

class WorkoutCreate(LoginRequiredMixin, CreateView):
  model = Workout
  fields = '__all__'

class WorkoutUpdate(LoginRequiredMixin, UpdateView):
  model = Workout
  fields = '__all__'

class WorkoutDelete(LoginRequiredMixin, DeleteView):
  model = Workout
  success_url = '/workouts'




class ExerciseList(LoginRequiredMixin, ListView):
  model = Exercise
  context_object_name = 'exercises'

class ExerciseDetail(LoginRequiredMixin, DetailView):
  model = Exercise
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    exercise_form = ExerciseForm()
    context["exercise_form"] = exercise_form
    return context

class ExerciseCreate(LoginRequiredMixin, CreateView):
  model = Exercise
  fields = '__all__'

class ExerciseUpdate(LoginRequiredMixin, UpdateView):
  model = Exercise
  fields = '__all__'

class ExerciseDelete(LoginRequiredMixin, DeleteView):
  model = Exercise
  success_url = '/workouts'
  
