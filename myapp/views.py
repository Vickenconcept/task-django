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
    todos = TodoList.objects.filter(user=request.user)
    return render(request, 'myapp/pages/todo/index.html', {'todos': todos})

# View for creating a new Todo
@login_required
def create_todo(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if not name.strip():
            messages.error(request, "Title Required")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        todo = TodoList.objects.create(user=request.user, name=name)
        return redirect('todo_list')
    return render(request, 'myapp/pages/todo/create.html')

def show_todo(request, id):
    
    # todo = TodoList.objects.get(id=id)
    todo = get_object_or_404(TodoList, id=id, user=request.user)
    return render(request, 'myapp/pages/todo/show.html', {'todo': todo})

# View to mark item as complete
@login_required
def toggle_complete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.complete = not item.complete
    item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# View to delete a Todo
@login_required
def delete_todo(request, todo_id):
    todo = TodoList.objects.get(id=todo_id)
    todo.delete()
    return redirect('todo_list')

def create_list(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        text = request.POST.get('text')

        # Validate that both id and text are provided
        if not id:
            messages.error(request, "TodoList ID is required.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('some_error_page')  # Redirect to an error page or the same page

        if not text.strip() :
            messages.error(request, "Title is required.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('some_error_page')  

        try:
            todo = get_object_or_404(TodoList, id=id)

            item = todo.items.create(text=text)  

            return redirect('show_todo', id=id)

        except TodoList.DoesNotExist:
            messages.error(request, "TodoList not found.")

    # Render the form for GET requests
    return redirect('show_todo', id=id)

def delete_item(request, item_id):
    try:
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        messages.success(request, 'Item deleted successfully!')  
    except Exception as e:
        messages.error(request, f'Error deleting item: {str(e)}')  

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))