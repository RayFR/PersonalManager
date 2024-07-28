from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("todos/", views.todos, name="Todos"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("manage/", views.manage, name="manage"),
]