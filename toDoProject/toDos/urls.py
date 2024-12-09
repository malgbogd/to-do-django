"""
URL configuration for toDoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from toDos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.todo_list, name = 'main'),
    path('details/<int:todo_id>', views.ToDoDetails.as_view(), name = 'details'),
    path('users/', views.UsersListCreate.as_view(), name = 'users'),
    path('add-to-do/', views.add_todo, name = 'add_to_do'),
    path('create-todo', views.create_todo, name = 'create_todo'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name = 'logout_view'),
    path('delete/<int:todo_id>/', views.ToDoDelete.as_view(), name = 'delete'),
    path('edit/<int:todo_id>/' , views.edit_todo, name = 'edit'),
    path('save-edit/<int:todo_id>/', views.save_edited_todo, name = 'save_edits'),
    path('check-box-edit/<int:todo_id>/', views.checkbox_edit, name ='check_box_edit'),
    path('profile/', views.profile_view_update, name = 'profile'),
    path('add-subtask/<int:todo_id>/', views.add_subtask, name='add_subtask'),
    path('delete-subtask/<int:subtask_id>', views.delete_subtask, name = "delete_subtask"),
    path('update-subtask/<int:subtask_id>', views.update_subtask, name = "update_subtask")
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
