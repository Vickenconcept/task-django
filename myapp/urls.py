from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/create', views.create_todo, name='create_todo'),
    path('todos/<int:id>/', views.show_todo, name='show_todo'),
    path('todos/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('todos/toggle-complete/<int:item_id>', views.toggle_complete, name='toggle_complete'),
    path('list/create/', views.create_list, name='create_list'),
    path('list/<int:item_id>', views.delete_item, name='delete_item'),
]
