from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView 
from .models import Workout, Exercise
from .forms import ExerciseForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

  
  
class WorkoutList(ListView):
  model = Workout
  context_object_name = 'workouts'

class WorkoutDetail(DetailView):
  model = Workout
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    exercise_form = ExerciseForm()
    context["exercise_form"] = exercise_form
    return context

class WorkoutCreate(CreateView):
  model = Workout
  fields = '__all__'

class WorkoutUpdate(UpdateView):
  model = Workout
  fields = '__all__'

class WorkoutDelete(DeleteView):
  model = Workout
  success_url = '/workouts'
  
def add_exercise(request,pk):
  form = ExerciseForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.workout_id = pk
    new_feeding.save()
  return redirect('workouts_detail', pk=pk)