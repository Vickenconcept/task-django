from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from ..models import TodoList  # Import your TodoList model

class TodoService:
    
    @staticmethod
    def todo_list(request):
        todos = TodoList.objects.filter(user=request.user)
        return render(request, 'myapp/pages/todo/index.html', {'todos': todos})
    @staticmethod
    def create_todo(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            
            if not name.strip():
                messages.error(request, "Title Required")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
            todo = TodoList.objects.create(user=request.user, name=name)
            return redirect('todo_list')
        return render(request, 'myapp/pages/todo/create.html')

    @staticmethod
    def show_todo(request, id):
        todo = get_object_or_404(TodoList, id=id, user=request.user)
        return render(request, 'myapp/pages/todo/show.html', {'todo': todo})
   
    
    @staticmethod
    def delete_todo(request, todo_id):
        todo = TodoList.objects.get(id=todo_id)
        todo.delete()
        messages.success(request,"Deleted Successfully")
        return redirect('todo_list')
    
    @staticmethod
    def bulk_delete_todos(request):
        if request.method == 'POST':
            todo_ids = request.POST.getlist('todo_ids') 
            if todo_ids: 
                TodoList.objects.filter(id__in=todo_ids).delete()
                messages.success(request, "TodoList Deleted Successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        return HttpResponse("Invalid request", status=400)