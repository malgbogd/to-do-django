from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils import timezone
from .models import ToDo, SubToDo
from .serializers import ToDoSerializer, UserSerializer, SubtaskSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pyexpat.errors import messages

# Create your views here.

def todo_list(request):

    if request.user.is_authenticated:
        to_dos = ToDo.objects.filter(author=request.user)

    else: 
        to_dos = ToDo.objects.filter(author=None)
    
    not_completed = to_dos.filter(completion=False).count()
    return render (request, 'main.html',{"todos":to_dos, 'not_completed':not_completed })

def add_todo(request):
    print(f"User logged in: {request.user.is_authenticated}")
    return render(request, 'create.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('main')

def save_edited_todo(request, todo_id):
    to_do = get_object_or_404(ToDo, id = todo_id)

    to_do.title = request.POST.get('title')
    to_do.text = request.POST.get('text')

    if 'image' in request.FILES:
        to_do.image=request.FILES.get('image')

    to_do.save()

    return redirect(reverse('details', kwargs = {"todo_id":to_do.id}))

def edit_todo(request, todo_id):
    to_do =get_object_or_404(ToDo, id = todo_id)
    return render(request, 'edit.html' ,{"todo": to_do})

def checkbox_edit(request, todo_id):
    if request.method == "POST":
        to_do =get_object_or_404(ToDo, id=todo_id)

        to_do.completion = not to_do.completion

        if to_do.completion:
            to_do.completion_date = timezone.now()
        else:
            to_do.completion_date = None
    
        to_do.save()

        if request.user.is_authenticated:
            to_dos = ToDo.objects.filter(author=request.user)

        else: 
            to_dos = ToDo.objects.filter(author=None)
        
        not_completed = to_dos.filter(completion=False).count()

        return JsonResponse({
            'status':'success',
            'completion': to_do.completion,
            'completion_date': to_do.completion_date.strftime('%d %b %Y %H:%M') if to_do.completion else None,
            'not_completed':not_completed,
        })
    return JsonResponse({'status':'error', 'message': 'Invalid request method'}, status = status.HTTP_400_BAD_REQUEST)

def add_subtask(request, todo_id):
    print("Metoda żądania:", request.method)
    print("Otrzymane dane:", request.POST)

    if request.method == 'POST':
        to_do = get_object_or_404(ToDo, id = todo_id)

        data = {
            'to_do': to_do.id,
            'title':request.POST.get('title'),
            'text': request.POST.get('text'),
            'completion': False,
        }
        serializer = SubtaskSerializer(data = data)
        if serializer.is_valid():
            subtask = serializer.save()
            return JsonResponse({
                "status":"success",
                "subtask": {
                    "id": subtask.id,
                    "title":subtask.title,
                    "text":subtask.text,
                    "to_do":subtask.to_do.id,
                    "completion":subtask.completion,
                }
            })
        else:
            return JsonResponse({"status":"error", "errors":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"status":"error", "message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

def update_subtask(request, subtask_id):
    subtask = get_object_or_404(SubToDo, id=subtask_id)
    title = request.POST.get('title')
    text = request.POST.get('text')
    completion = request.POST.get('completion', False)
    completion = True if completion=="on" else False

    if not title or not text:
        return JsonResponse({"status": "error", "message": "Title and text are required."}, status=status.HTTP_400_BAD_REQUEST)

    subtask.title = title
    subtask.text = text
    subtask.completion = completion

    subtask.save()
    
    return JsonResponse({
                "status":"success",
                "subtask": {
                    "id": subtask.id,
                    "title":subtask.title,
                    "text":subtask.text,
                    "to_do":subtask.to_do.id,
                    "completion":subtask.completion,
                }
            }, status = status.HTTP_200_OK)

def update_subtask_completion(request, subtask_id):
    subtask = get_object_or_404(SubToDo, id=subtask_id)
    subtask.completion = not subtask.completion
    subtask.save()
    
    return JsonResponse({
                "status":"success",
                "subtask": {
                    "id": subtask.id,
                    "title":subtask.title,
                    "text":subtask.text,
                    "to_do":subtask.to_do.id,
                    "completion":subtask.completion,
                }
            }, status = status.HTTP_200_OK)

def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubToDo, id = subtask_id)
    subtask.delete()
    return JsonResponse({"status":"success"})

def profile_view(request):
    return render(request, 'profile.html')

def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new-password')
        password_check = request.POST.get('password-check')

        user = request.user

        if new_password and new_password != password_check:
            return render(request, 'profile.html', {"messages":"Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if username:
            user.username = username

        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()
        
        return render(request, 'profile.html',{"messages":"Profile updated successfully."}, status = status.HTTP_200_OK)

    return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

def create_todo(request):
        data = {
            'title':request.POST.get('title'),
            'text': request.POST.get('text'),
            'image':request.FILES.get('image'),
        }

        if request.user.is_authenticated:
            data['author'] = request.user

        serializer = ToDoSerializer(data = data)
        if serializer.is_valid():
            to_do = serializer.save()
            return redirect(reverse('details', kwargs = {"todo_id":to_do.id}))
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return render(request,'register.html',{"messages":"Your profile has been deleted successfully."})
    
class ToDoDetails(APIView):
    def get(self, request, todo_id):
        to_do = get_object_or_404(ToDo, id = todo_id)
        subtasks = to_do.subtasks.all()
        serializer = ToDoSerializer(to_do)
        serializerSubtask = SubtaskSerializer(subtasks, many =True)
        return render(request, 'details.html',{"todo":to_do,"subtasks":serializerSubtask.data})
    
class ToDoDelete(View):
    def post(self, request, todo_id):
        to_do = get_object_or_404(ToDo, id=todo_id)
        to_do.delete()

        redirect_url = request.POST.get('redirect')
        if redirect_url:
            return JsonResponse({'status': 'redirect', 'url': redirect_url})

        return JsonResponse({'status':'success', 'todo_id': todo_id})
    
class UsersListCreate(APIView):
    def get(self, request):

        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        action = request.data.get('action')

        if not action:
            return Response({"error":"Action is required"}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'login':
            username =request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response({"error":"Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                request.session['message'] = 'Successfully logged in'

                to_dos = ToDo.objects.filter(author=None)
                for to_do in to_dos:
                    to_do.author= request.user
                    to_do.save()

                return redirect(reverse("main"))
            else:
                return render(request, 'login.html', {'error_message': "Incorrect username or password"})

        elif action == 'register':
            password = request.data.get('password')
            password_check = request.data.get('password-check')

            if password != password_check:
                return render(request, 'register.html', {'error_message': 'There was an error with the registration form'})

            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return render(request, 'login.html', {"user": serializer.data}, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
    
