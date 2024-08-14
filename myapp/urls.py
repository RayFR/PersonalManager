from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("register/", views.register, name="register"),
    path("", views.dashboard, name="dashboard"),
    path("manage/", views.manage, name="manage"),
    path("settings/", views.settings, name="settings"),
    path('task/<int:task_id>/toggle/', views.toggle_task_completion, name='toggle_task_completion'), # url pattern toggles the completion of specific task. The task_id placeholder is passed through the view
    path('habit/<int:habit_id>/toggle/', views.toggle_habit_completion, name='toggle_habit_completion'),
]