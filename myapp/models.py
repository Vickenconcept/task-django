# from django.db import models

# # Create your models here.
# class TodoList(models.Model):
#     name = models.CharField(max_length=200)
    
#     def __str__(self):
#         return self.name
    
# class Item(models.Model):
#     todolst = models.ForeignKey(TodoList, on_delete=models.CASCADE)
#     text = models.CharField(max_length=300)
#     complete = models.BooleanField()
    
#     def __str__ (self):
#         return self.text
    
    
from django.db import models
from django.contrib.auth.models import User

# Todo List Model
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Todo Item Model
class Item(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=300)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.text
