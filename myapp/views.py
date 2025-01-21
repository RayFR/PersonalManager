from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Habit, Goal
from .forms import GoalForm, RegistrationForm, LoginForm, TaskForm, HabitForm, HabitDashboardForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import calendar
from calendar import HTMLCalendar
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, "register.html", {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, current_day, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_day = current_day

    # Override the formatday method to highlight the current day
    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # Empty days
        elif day == self.current_day:
            return f'<td class="today">{day}</td>'  # Highlight the current day
        else:
            return f'<td>{day}</td>'  # Regular day

def dashboard(request):   
    now = datetime.now() # gets current datetime
    current_year = now.year
    current_month = now.month
    current_day = now.day
    
    cal = CustomHTMLCalendar(current_day).formatmonth(current_year, current_month)
    
    habitForm = HabitDashboardForm(request.POST or None)
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit = get_object_or_404(Habit, id=habit_id)
        habitForm = HabitDashboardForm(data=request.POST, instance=habit)
        if habitForm.is_valid():
            habitForm.save()
            return redirect('dashboard')

    try:
        tasks = Task.objects.filter(user=request.user).order_by('-priority').values()
        tasks = tasks.order_by("completed")
        habits = Habit.objects.filter(user=request.user).order_by('completed')
        goals = Goal.objects.filter(user=request.user)
    except TypeError:
        return redirect('login')
    print(f"Goals: {goals}")
    return render(request, "dashboard.html", {
        "tasks": tasks, 
        "habits": habits, 
        "habitForm": habitForm, 
        "goals": goals,
        'calendar': cal,
        'current_day': current_day,
        'current_month': current_month,
        'current_year': current_year,})
    
def manage(request):
    goalForm = GoalForm(request.POST or None)
    taskForm = TaskForm(request.POST or None, user=request.user)
    habitForm = HabitForm(request.POST or None)

    if request.method == 'POST':
        if 'create_goal' in request.POST:
            goalForm = GoalForm(data=request.POST)
            if goalForm.is_valid():
                goal = goalForm.save(commit=False)
                goal.user = request.user
                goal.save()
                messages.success(request, 'Goal created successfully!')
                return redirect('manage')
            else:
                messages.error(request, 'Failed to create goal.')

        if 'create_task' in request.POST:
            taskForm = TaskForm(data=request.POST, user=request.user)
            if taskForm.is_valid():
                task = taskForm.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('manage')

        if 'create_habit' in request.POST:
            habitForm = HabitForm(data=request.POST)
            if habitForm.is_valid():
                habit = habitForm.save(commit=False)
                habit.user = request.user
                habit.save()
                return redirect('manage')

    try: 
        goals = Goal.objects.filter(user=request.user)
    except TypeError:
        return redirect('login')

    return render(request, "manage.html", {
        'goalForm': goalForm,
        'taskForm': taskForm,
        'habitForm': habitForm,
        'goals': goals,
    })

def settings(request):
    return render(request, "settings.html")

def toggle_task_completion(request, task_id): # takes the request and the task id value as parameters
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.completed = not task.completed # reverses whatever the value of task.completed is
        task.save() # saves task
        return redirect('dashboard')
    
    return render(request, 'task/toggle_completion.html', {'task': task}) # passes task context and the html rendering of the updated task values

def toggle_habit_completion(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)

    if request.method == 'POST':
        habit.completed = not habit.completed
        habit.save()
        return redirect('dashboard')
    
    return render(request, 'habit/toggle_completion.html', {'habit': habit})