from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['UserId','UserName', 'Email']

@admin.register(Question)
class TodoModelAdmin(admin.ModelAdmin):
    list_display=['QuestionId', 'UserId', 'DateOfAdding', 'Status']

@admin.register(Answer)
class TodoModelAdmin(admin.ModelAdmin):
    list_display=['AnswerId', 'UserId', 'QuestionId', 'DateOfAdding']