from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

# THIS CLASS MODEL ALLOWS FOR USERS TO BE MANAGED (CREATED) - ALLOWS FOR BOTH STANDARD USERS AND SUPERUSERS (ADMINS) TO BE CREATED

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError('Enter An valid email')
        if not username:
            raise ValueError('enter correct Username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,username,email,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password= password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        

# THIS CLASS MODEL ALLOWS FOR THE USERS DATA TO BE INITIALISED IN DATABASE - IT ALSO GIVES DIFFERENT PERMISSIONS TO USERS

class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    
    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

# User var

User = get_user_model()

# TASK CLASS MODEL USED TO STORE TASKS IN DB - TAKES IN A FOREIGN KEY OF THE USER IN ORDER TO GET DATA FROM SPECIFIC USERS

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    goal = models.ForeignKey('Goal', related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1250)
    dateDue = models.DateField()
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# HABIT CLASS MODEL USED TO STORE HABITS IN DB 

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)
    
# GOALS CLASS MODEL USED TO STORE GOALS THAT HAVE SUB TASKS

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1250, null=True, blank=True)
    dateDue = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

