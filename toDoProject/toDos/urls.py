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
    path('profile/', views.profile_view, name = 'profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/update/', views.UpdateProfile.as_view(), name = 'update_profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name = 'logout_view'),
    path('users/', views.UsersListCreate.as_view(), name = 'users'),
    path('', views.todo_list_view, name = 'main'),
    path('todo/add/', views.add_todo_view, name = 'add_to_do'),
    path('todo/create', views.CreateTodo.as_view(), name = 'create_todo'),
    path('todo/details/<int:todo_id>', views.todo_details, name = 'details'),
    path('todo/delete/<int:todo_id>/', views.ToDoDelete.as_view(), name = 'delete'),
    path('todo/edit/<int:todo_id>/' , views.edit_todo, name = 'edit'),
    path('todo/save-edits/<int:todo_id>/', views.save_edited_todo, name = 'save_edits'),
    path('todo/toggle/<int:todo_id>/', views.ToggleTodoCompletion.as_view(), name ='toggle_todo'),
    path('subtask/add/<int:todo_id>/', views.AddSubtask.as_view(), name='add_subtask'),
    path('subtask/delete/<int:subtask_id>', views.delete_subtask, name = "delete_subtask"),
    path('subtask/update/<int:subtask_id>', views.UpdateSubtask.as_view(), name = "update_subtask"),
    path('subtask/toggle/<int:subtask_id>', views.ToggleSubtaskCompletion.as_view, name = "toggle_subtask_completion"),
    path('give-reward/', views.GiveReward.as_view(), name = 'give_reward')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
