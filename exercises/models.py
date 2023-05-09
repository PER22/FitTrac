from django.db import models
from django.urls import reverse

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    difficulty_rating = models.IntegerField()

  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
    def __str__(self):
      return f'{self.name} ({self.id})'

    def get_absolute_url(self):
      return reverse('exercise_detail', kwargs={'pk': self.id})
