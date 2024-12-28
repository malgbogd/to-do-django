import json
import os
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from django.utils import timezone
from .models import ToDo, SubToDo, UserReward
from .serializers import ToDoSerializer, UserSerializer, SubtaskSerializer, RewardSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv
load_dotenv()

CAT_KEY = os.environ['CAT_API_KEY']
# Create your views here.

def todo_list_view(request):

    if request.user.is_authenticated:
        to_dos = ToDo.objects.filter(author=request.user)

    else: 
        to_dos = ToDo.objects.filter(author=None)
    
    not_completed = to_dos.filter(completion=False).count()
    return render (request, 'main.html',{"todos":to_dos, 'not_completed':not_completed })

def add_todo_view(request):
    return render(request, 'create.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('main')

def save_edited_todo(request, todo_id):
    to_do = get_object_or_404(ToDo, id = todo_id)

    to_do.title = request.POST.get('title')
    to_do.text = request.POST.get('text')

    if 'remove_image' in request.POST and 'image' not in request.FILES:
        to_do.image.delete(save=False)
        to_do.image = None

    if 'image' in request.FILES:
        to_do.image=request.FILES.get('image')

    to_do.save()

    return redirect(reverse('details', kwargs = {"todo_id":to_do.id}))

def edit_todo_view(request, todo_id):
    to_do =get_object_or_404(ToDo, id = todo_id)
    return render(request, 'edit.html' ,{"todo": to_do})

def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubToDo, id = subtask_id)
    subtask.delete()
    return JsonResponse({"status":"success"})

def profile_view(request):
    rewards = UserReward.objects.filter(user=request.user)
    return render(request, 'profile.html',{'rewards':rewards})

def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return render(request,'register.html',{"messages":"Your profile has been deleted successfully."})

def todo_details_view(request, todo_id):
    to_do = get_object_or_404(ToDo, id = todo_id)
    subtasks = to_do.subtasks.all()
    serializer = ToDoSerializer(to_do)
    serializerSubtask = SubtaskSerializer(subtasks, many =True)
    return render(request, 'details.html',{"todo":to_do,"subtasks":serializerSubtask.data})

def create_todo(request):
        data = {
            'title':request.POST.get('title'),
            'text': request.POST.get('text'),
            'image':request.FILES.get('image'),
            'author':None,
        }

        if request.user.is_authenticated:
            data['author'] = request.user.id

        serializer = ToDoSerializer(data = data, context={'request':request})
        if serializer.is_valid():
            to_do = serializer.save()
            return redirect(reverse('details', kwargs = {"todo_id":to_do.id}))
        else:
            return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

class GiveReward(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        if request.method =="POST" :
            data = json.loads(request.body)
            image_url = data.get("url")

            if not image_url:
                return JsonResponse({"error": "Image URL is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                'user':request.user.id,
                'image_url': image_url,
            }
            serializer = RewardSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
            return JsonResponse({'messages':'Image saved', 'reward':serializer.data}, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
 
class ToDoDelete(View):
    def post(self, request, todo_id):
        to_do = get_object_or_404(ToDo, id=todo_id)
        to_do.delete()

        if request.user.is_authenticated:
                to_dos = ToDo.objects.filter(author=request.user)

        else: 
            to_dos = ToDo.objects.filter(author=None)

        not_completed = to_dos.filter(completion=False).count()

        redirect_url = request.POST.get('redirect')
        if redirect_url:
            return JsonResponse({'status': 'redirect', 'url': redirect_url})

        return JsonResponse({'status':'success', 'todo_id': todo_id, "not_completed":not_completed})
    
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
                return render(request, 'login.html', {"user": serializer.data, "message":"User created successfully"}, status = status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

class ToggleTodoCompletion(View):
    def post(self, request,todo_id):
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
    
class AddSubtask(View):
    def post (self, request, todo_id):
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
    
class UpdateSubtask(View):
    def post (self,request, subtask_id):
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

class ToggleSubtaskCompletion(View):
    def post (self,request, subtask_id):
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

class UpdateProfile(View):
    def post (self,request):
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