from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView 
from .models import Exercise

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

  
  
class ExerciseList(ListView):
  model = Exercise

class ExerciseDetail(DetailView):
  model = Exercise

class ExerciseCreate(CreateView):
  model = Exercise
  fields = '__all__'

class ExerciseUpdate(UpdateView):
  model = Exercise
  fields = '__all__'

class ExerciseDelete(DeleteView):
  model = Exercise
  success_url = '/exercises'