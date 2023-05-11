from django.db import models
from django.urls import reverse

WORKOUT_GEAR = (
  ('N', 'no equipment'),
  ('B','barbells'),
  ('Y','a yoga mat'),
  ('D','dumbells'),
  ('R', 'resistance bands'),
  ('T', 'TRX bands')
)

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=250, default="")
    difficulty_rating = models.IntegerField(default=5)

  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
    def __str__(self):
      return f'{self.name} ({self.id})'

    def get_absolute_url(self):
      return reverse('workout_detail', kwargs={'pk': self.id})

class Exercise(models.Model):
  name = models.CharField(max_length=50, default="")
  equipment = models.CharField(
    max_length=1, 
    choices=WORKOUT_GEAR,
    default=WORKOUT_GEAR[0][0]
  )
  description = models.TextField(max_length=250, default="")
  workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default="")
  
  def __str__(self):
    return f"{self.name} using {self.get_equipment_display()}" 