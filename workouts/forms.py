from django.forms import ModelForm, Select, ModelChoiceField
from .models import Exercise, Set, Workout, Profile

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'type', 'equipment', 'description']
        
        

class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['exercise', 'duration', 'weight', 'resistance', 'distance', 'time', 'reps']

    def __init__(self, *args, **kwargs):
        exercise_queryset = kwargs.pop('exercise_queryset',None)
        super().__init__(*args, **kwargs)
        if exercise_queryset:
            self.fields['exercise'].queryset = exercise_queryset
        

        
class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'difficulty_rating']
        
        
        
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic_url', 'bio']
        exclude = ['user', 'workouts', 'exercises']
        
    
        