import os
import uuid
import boto3
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Workout, Exercise, Set, Profile, User
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
  def get_queryset(self):
      user = self.request.user
      return super().get_queryset().filter(profiles__user=user)

class WorkoutDetail(LoginRequiredMixin, DetailView):
  model = Workout
  def get_queryset(self):
    return super().get_queryset()
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    exercise_form = ExerciseForm()
    context["exercise_form"] = exercise_form
    
    workout = self.get_object()
    sets = workout.sets.all()
    context["sets"] = sets
    return context

class WorkoutCreate(LoginRequiredMixin, CreateView):
  model = Workout
  form_class = WorkoutForm
  def form_valid(self, form):
    profile = self.request.user.profiles
    form.instance.save() 
    form.instance.profiles.set([profile])
    form.instance.save() 
    return super().form_valid(form)

class WorkoutUpdate(LoginRequiredMixin, UpdateView):
    model = Workout
    fields = '__all__'
    def get_context_data(self, **kwargs):
      profile = self.request.user.profiles
      context = super().get_context_data(**kwargs)
      workout = self.object
      context["profile"] = profile
      context['sets'] = workout.sets.all()
      context['set_form'] = SetForm(exercise_queryset=Exercise.objects.filter(profiles=profile))
      return context

class WorkoutDelete(LoginRequiredMixin, DeleteView):
  model = Workout
  success_url = '/workouts'




class ExerciseList(LoginRequiredMixin, ListView):
  model = Exercise
  context_object_name = 'exercises' 
  def get_queryset(self):
      user = self.request.user
      return super().get_queryset().filter(profiles__user=user)
  
class ExerciseDetail(LoginRequiredMixin, DetailView):
  model = Exercise
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    exercise_form = ExerciseForm()
    context["exercise_form"] = exercise_form
    return context

class ExerciseCreate(LoginRequiredMixin, CreateView):
  model = Exercise
  form_class = ExerciseForm
  def form_valid(self, form):
      profile = self.request.user.profiles
      form.instance.save()
      form.instance.profiles.add(profile)
      return super().form_valid(form)

class ExerciseUpdate(LoginRequiredMixin, UpdateView):
  model = Exercise
  fields = '__all__'

class ExerciseDelete(LoginRequiredMixin, DeleteView):
  model = Exercise
  success_url = '/workouts'
  

def add_set(request, workout_pk, exercise_pk):
    workout = get_object_or_404(Workout, pk=workout_pk)
    exercise = get_object_or_404(Exercise, pk=exercise_pk)
    if request.method == 'POST':
        form = SetForm(request.POST, initial={'exercise': exercise, 'workout': workout})
        
        if form.is_valid():
            new_set = form.save(commit=False)
            new_set.exercise = exercise
            new_set.workout = workout
            new_set.save()
            workout.sets.add(new_set)
            workout.save()
            return redirect('workout_update', pk=workout.pk)
    else:
        form = SetForm()
    
    return redirect('workout_update', pk=workout.pk)
  
  
  
class ProfileDetail(LoginRequiredMixin, DetailView):
  model = Profile
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile_form = ProfileForm()
    context["profile_form"] = profile_form
    return context

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  fields = ['profile_pic_url', 'bio']

class ProfileDelete(LoginRequiredMixin, DeleteView):
  model = Profile
  success_url = '/workouts'


@login_required
def add_photo(request, profile_id):
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, profile_id = profile_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', cat_id=cat_id)
  