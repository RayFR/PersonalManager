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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, "register.html", {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        print('request method is POST')
        if form.is_valid():
            print('form is valid')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email,password=password)
            if user is not None:
                print('user is true')
                login(request,user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})