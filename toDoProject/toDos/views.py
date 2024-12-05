from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import ToDo, SubToDo
from .serializers import ToDoSerializer, UserSerializer, SubtaskSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pyexpat.errors import messages

# Create your views here.
# def main(request):
#     to_dos = ToDo.objects.all()
#     return render (request, 'main.html',{"todos":to_dos})
def addToDo(request):
    print(f"User logged in: {request.user.is_authenticated}")
    return render(request, 'create.html')

def loginRegister(request):
    return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return redirect('main')

class ToDosListCreate(APIView):
    def get(self, request):
        print(f"User logged in: {request.user.is_authenticated}")

        to_dos = ToDo.objects.filter()

        # if request.user.is_authenticated:
        #     to_dos = ToDo.objects.filter(author=request.user)

        # else: 
        #     to_dos = ToDo.objects.filter(author=None)
        
        not_complited = ToDo.objects.filter(complition=False).count()
        return render (request, 'main.html',{"todos":to_dos, 'not_complited':not_complited })

    def post(self, request):
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

class ToDoDetails(APIView):
    def get(self, request, todo_id):
        print(f"User logged in: {request.user.is_authenticated}")
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
            username =request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)

            if not username or not password:
                return Response({"error":"Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            

            if user is not None:
                login(request, user)
                request.session['message'] = 'Successfully logged in'

                to_dos = ToDo.objects.filter(author=None)

                for to_do in to_dos:
                    to_do["author"] = request.user

                return redirect(reverse("main"))
            else:
                return Response({"error": "Incorrect login details"}, status=status.HTTP_401_UNAUTHORIZED)

        elif action == 'register':
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return render(request, 'login.html', {"user": serializer.data}, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

