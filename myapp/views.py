from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem, Task, Habit, Goal
from .forms import GoalForm, RegistrationForm, LoginForm, TaskForm, HabitForm, HabitDashboardForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

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
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def dashboard(request):
    habitForm = HabitDashboardForm(request.POST or None)
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit = get_object_or_404(Habit, id=habit_id)
        habitForm = HabitDashboardForm(data=request.POST, instance=habit)
        if habitForm.is_valid():
            habitForm.save()
            return redirect('dashboard')

    tasks = Task.objects.all().order_by('-priority').values()
    habits = Habit.objects.all()
    goals = Goal.objects.all()
    return render(request, "dashboard.html", {"tasks": tasks, "habits": habits, "habitForm": habitForm, "goals": goals})

def manage(request):
    goalForm = GoalForm(request.POST or None)
    taskForm = TaskForm(request.POST or None)
    habitForm = HabitForm(request.POST or None)

    if request.method == 'POST':
        if 'create_goal' in request.POST:
            goalForm = GoalForm(data=request.POST)
            if goalForm.is_valid():
                goalForm.save()
                return redirect('manage')

        if 'create_task' in request.POST:
            taskForm = TaskForm(data=request.POST)
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

    goals = Goal.objects.filter(user=request.user)

    return render(request, "manage.html", {
        'goalForm': goalForm,
        'taskForm': taskForm,
        'habitForm': habitForm,
        'goals': goals,
    })
