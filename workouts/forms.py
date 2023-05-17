from django.forms import ModelForm, Select, ModelChoiceField
from .models import Exercise, Set, Workout, Profile

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'type', 'equipment', 'description']
        
        

class SetForm(ModelForm):
    exercise = ModelChoiceField(
        queryset=None,
        widget=Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Set
        fields = ['exercise', 'duration', 'weight', 'resistance', 'distance', 'time', 'reps']

    def __init__(self, *args, **kwargs):
        exercise_queryset = kwargs.pop('exercise_queryset')
        super().__init__(*args, **kwargs)
        self.fields['exercise'].queryset = exercise_queryset

        
class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'difficulty_rating']
        
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic_url', 'bio', 'workouts', 'exercises']
        
    
        