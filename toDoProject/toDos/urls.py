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
    path('', views.ToDosListCreate.as_view(), name = 'main'),
    path('<int:todo_id>', views.ToDoDetails.as_view(), name = 'details'),
    path('users/', views.UsersListCreate.as_view(), name = 'users'),
    path('add-to-do/', views.addToDo, name = 'add_to_do'),
    path('login/', views.loginRegister, name='login'),
    path('logout/', views.logoutView, name = 'logoutView'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
