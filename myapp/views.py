from django.shortcuts import render, HttpResponse, redirect
from .models import TodoItem
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate  # add to imports
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, "register.html", {'form': form})

def login_view(request):
    form = LoginForm()
    message = ''
    logged = 'You are not logged in.'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate using email and password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("user found")
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                logged = f'You are logged in as {user.username}'
            else:
                print("user not found")
                message = 'Not logged in!'
    return render(request, 'login.html', context={'form': form, 'message': message, 'logged': logged})