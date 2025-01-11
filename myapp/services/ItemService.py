from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from ..models import TodoList, Item

class ItemService:
    
    @staticmethod
    def toggle_complete(request, item_id):
        item = get_object_or_404(Item, id=item_id)
        item.complete = not item.complete
        item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    @staticmethod
    def create_list(request):
        if request.method == 'POST':
            id = request.POST.get('id')
            text = request.POST.get('text')

            if not id:
                messages.error(request, "TodoList ID is required.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if not text.strip() :
                messages.error(request, "Title is required.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            try:
                todo = get_object_or_404(TodoList, id=id)

                item = todo.items.create(text=text)  

                return redirect('show_todo', id=id)

            except TodoList.DoesNotExist:
                messages.error(request, "TodoList not found.")

        return redirect('show_todo', id=id)
    
    @staticmethod
    def delete_item(request, item_id):
        try:
            item = get_object_or_404(Item, id=item_id)
            item.delete()
            messages.success(request, 'Item deleted successfully!')  
        except Exception as e:
            messages.error(request, f'Error deleting item: {str(e)}')  

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))