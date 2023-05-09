from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('exercises/', views.ExerciseList.as_view(), name='exercise_list'),
  path('exercises/<int:pk>/', views.ExerciseDetail.as_view(), name='exercise_detail'),
  path('exercises/create/', views.ExerciseCreate.as_view(), name='exercise_create'),
  path('exercises/<int:pk>/update/', views.ExerciseUpdate.as_view(), name='exercise_update'),
  path('exercises/<int:pk>/delete/', views.ExerciseDelete.as_view(), name='exercise_delete'),
]