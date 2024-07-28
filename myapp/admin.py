from django.contrib import admin
from .models import TodoItem, User, Task

# Register your models here.
admin.site.register(TodoItem) 
admin.site.register(User)
admin.site.register(Task)
