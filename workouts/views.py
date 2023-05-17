import os
import uuid
import boto3
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Workout, Exercise, Set, Profile, User, WorkoutExercise, ProfileWorkout
from .forms import ExerciseForm, SetForm, WorkoutForm, ProfileForm

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
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
  
  
class WorkoutList(LoginRequiredMixin, ListView):
  model = Workout
  context_object_name = 'workouts'

class WorkoutDetail(LoginRequiredMixin, DetailView):
  model = Workout
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    exercise_form = ExerciseForm()
    context["exercise_form"] = exercise_form
    return context

class WorkoutCreate(LoginRequiredMixin, CreateView):
  model = Workout
  fields = '__all__'

class WorkoutUpdate(LoginRequiredMixin, UpdateView):
    model = Workout
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.object
        sets = workout.sets.all() 
        context['sets'] = sets
        context['set_form'] = SetForm()
        return context

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
  

def add_set(request, workout_id, exercise_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            new_set = form.save(commit=False)
            new_set.save()
            
            workout_exercise, _ = WorkoutExercise.objects.get_or_create(workout=workout)
            workout_exercise.sets.add(new_set)
            
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = SetForm()
    
    return redirect('workout_detail', pk=workout.pk)