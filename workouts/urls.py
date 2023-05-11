from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts/', views.WorkoutList.as_view(), name='workout_list'),
  path('workouts/<int:pk>/', views.WorkoutDetail.as_view(), name='workout_detail'),
  path('workouts/create/', views.WorkoutCreate.as_view(), name='workout_create'),
  path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workout_update'),
  path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete'),
  path('cats/<int:pk>/add_exercise/', views.add_exercise, name='add_exercise'),
]