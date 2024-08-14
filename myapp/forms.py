from django import forms
from .models import User, Task, Habit, Goal

class RegistrationForm(forms.ModelForm): # ModelForm which adds new user data via input form 
    class Meta:
        model = User # defines what model to configure - in this case its the User model which has been imported ^
        fields = ['email', 'password', 'username'] # fields specified for the form
        widgets = {
            'password': forms.PasswordInput(), # this ensures the password is input with password logic (dots for chars)
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128)

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['goal', 'name', 'description', 'dateDue', 'priority']
        widgets = {
            'dateDue': DateInput(),
        }
    
    goal = forms.ModelChoiceField(
        queryset=Goal.objects.all(),
        empty_label="Select a goal",
        widget=forms.Select(),
        required=False,
    )

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'dateDue']
        widgets = {
            'dateDue': DateInput(),
        }

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name']

class HabitDashboardForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['completed']
        widgets = {
            'completed': forms.CheckboxInput(),
        }

class TaskCompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["completed"]

