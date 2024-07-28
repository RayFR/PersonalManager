from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import TodoItem, Task, Habit, Goal
from .forms import GoalForm, RegistrationForm, LoginForm, TaskForm, HabitForm, HabitDashboardForm
from django.contrib.auth import login, authenticate  # add to imports
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html") # renders the html template (no context given)

def todos(request):
    items = TodoItem.objects.all() # gives a variable to the TodoItem models objects/values
    return render(request, "todos.html", {"todos": items}) # renders the html template with context of all of the TodoItem data

def register(request):
    if request.method == 'POST': # ensures the request has been issued with POST
        form = RegistrationForm(request.POST) # form variable storing the RegistrationForm data
        if form.is_valid(): # if form is input valid
            user = form.save(commit=False) # saves the user data but does not commit it yet to the database
            user.set_password(form.cleaned_data['password']) # sets the password as the form password data cleaned
            form.save() # saves user object to database
            return redirect('login') # redirects to the login page after successful registration
    else:
        form = RegistrationForm() # form variable is an empty form if not valid
    return render(request, "register.html", {'form': form}) # renders the html template with context of the form{'form': form}

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data = request.POST) # form variable with LoginForm form data
        print('request method is POST') 
        if form.is_valid(): # if form is valid
            print('form is valid')
            email = form.cleaned_data['email'] # email variable of the form inputs CLEANED email
            password = form.cleaned_data['password'] # password variable of the form inputs CLEANED password
            user = authenticate(email=email,password=password) # authenticates the user within a 'user' variable
            if user is not None:
                print('user is true')
                login(request,user) # user logged in with user variable
                return redirect('home') # redirects to the home page after login
    else:
        form = LoginForm() # empty login form if the request method isnt POST
    return render(request,'login.html',{'form':form})

def dashboard(request):
    habitForm = HabitDashboardForm(request.POST or None)
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit = get_object_or_404(Habit, id=habit_id)
        habitForm = HabitDashboardForm(data = request.POST, instance=habit)
                
        if habitForm.is_valid():
            habitForm.save()
            return redirect('dashboard')
        else:
            habitForm = HabitDashboardForm()

    tasks = Task.objects.all().order_by('-priority').values()
    habits = Habit.objects.all()
    goals = Goal.objects.all()
    return render(request, "dashboard.html", {"tasks": tasks, "habits": habits, "habitForm": habitForm, "goals": goals}) # passed the database items of Task model into context for dashboard

def manage(request):
    goalForm, taskForm, habitForm = GoalForm(request.POST or None), TaskForm(request.POST or None), HabitForm(request.POST or None) # FIXES THE UnboundLocalError because the form sometimes uses other request methods like GET not just POST
    if request.method == 'POST':
        goalForm, taskForm, habitForm = GoalForm(data = request.POST), TaskForm(data = request.POST), HabitForm(data = request.POST)
        
        if goalForm.is_valid():
            goalForm.save()
            return redirect('manage')
        else:
            goalForm = GoalForm()

        if taskForm.is_valid():
            taskForm.save()
            return redirect('manage')
        else:
            taskForm = TaskForm()

        if habitForm.is_valid():
            habitForm.save()
            return redirect('manage')
        else:
            habitForm = HabitForm()

    return render(request, "manage.html", {'goalForm':goalForm, 'taskForm':taskForm, 'habitForm':habitForm})