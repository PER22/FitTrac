from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path('', views.home, name='home'),   #Home page
  path('about/', views.about, name='about'), #About page
  
  
  path('workouts/', views.WorkoutList.as_view(), name='workout_list'), 
  path('workouts/<int:pk>/', views.WorkoutDetail.as_view(), name='workout_detail'),
  path('workouts/create/', views.WorkoutCreate.as_view(), name='workout_create'),
  path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workout_update'),
  path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete'),
  path('workouts/<int:pk>/add_set/', views.add_set, name='add_set'),
  
  
  path('exercises/', views.ExerciseList.as_view(), name='exercise_list'),
  path('exercises/<int:pk>/', views.ExerciseDetail.as_view(), name='exercise_detail'),
  path('exercises/create/', views.ExerciseCreate.as_view(), name='exercise_create'),
  path('exercises/<int:pk>/update/', views.ExerciseUpdate.as_view(), name='exercise_update'),
  path('exercises/<int:pk>/delete/', views.ExerciseDelete.as_view(), name='exercise_delete'),
  
  
  path('workouts/<int:pk>/exercises/<int:exercise_pk>/add_set/', views.add_set, name='add_set'),

  
  
  path('accounts/signup/', views.signup, name='signup'),
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]