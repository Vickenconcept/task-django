from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from .models import TodoList, Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .services.TodoService import TodoService  # Import the TodoService class
from .services.ItemService import ItemService  # Import the ItemService class



def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  
        return view_func(request, *args, **kwargs)
    return wrapped_view

def index(response, id):
    ls = TodoList.objects.get(id=id)
    return render(response, 'myapp/list.html', {"ls": ls})
    # return HttpResponse(f"<h1>{ls.name} <br> <br> <br>{ item.text}</h1>")

def home(response):
     return render(response, 'myapp/home.html', {})
 
@anonymous_required
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm(initial={'username': '', 'email': '', 'password1': '', 'password2': ''})
    return render(request, 'myapp/auth/register.html', {'form': form})


@anonymous_required
def login_view(request):  
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            return redirect('todo_list')
    else:
        form = AuthenticationForm(initial={'username': '', 'password': ''})
    return render(request, 'myapp/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def todo_list(request):
    return TodoService.todo_list(request)

# View for creating a new Todo
@login_required
def create_todo(request):
    return TodoService.create_todo(request)

@login_required
def show_todo(request, id):
    return TodoService.show_todo(request, id)

# View to delete a Todo
@login_required
def delete_todo(request, todo_id):
    return TodoService.delete_todo(request, todo_id)

@login_required
def todo_bulk_delete(request):
    return TodoService.bulk_delete_todos(request)
 
 # View to mark item as complete
@login_required
def toggle_complete(request, item_id):
    return ItemService.toggle_complete(request, item_id)
 

def create_list(request):
    return ItemService.create_list(request)
    

def delete_item(request, item_id):
   return ItemService.delete_item(request, item_id)