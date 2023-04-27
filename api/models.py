from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class UserAccountManager(BaseUserManager):
    use_in_migrations = True
    def create_superuser(self, UserName, Email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(UserName, Email, password, **other_fields)

    def create_user(self, UserName, Email,   password=None, **extra_fields):
        if not UserName:
            raise ValueError('Users must have an username address')
        Email = self.normalize_email(Email)
        user = self.model(UserName=UserName, Email = Email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    UserId=models.AutoField(primary_key=True)
    UserName=models.CharField(max_length=200, unique=True)
    Email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()
    
    USERNAME_FIELD = "UserName"
    REQUIRED_FIELDS = ['Email']

    
    def __str__(self):
        return self.UserName

class Question(models.Model):
    QuestionId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    QuestionText = models.TextField()
    DateOfAdding = models.DateTimeField()
    Status = models.BooleanField(default=False)
    def __str__(self):
        return self.QuestionId

class Answer(models.Model):
    AnswerId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    QuestionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    AnswerText = models.TextField()
    DateOfAdding = models.DateTimeField()
    def __str__(self):
        return self.AnswerId