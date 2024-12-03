from pyexpat.errors import messages
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect, render
from .models import ToDo, SubToDo
from .serializers import ToDoSerializer, UserSerializer, SubtaskSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# def main(request):
#     to_dos = ToDo.objects.all()
#     return render (request, 'main.html',{"todos":to_dos})
def addToDo(request):
    return render(request, 'create.html')

def loginRegister(request):
    return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return redirect('main')

class ToDosListCreate(APIView):
    def get(self, request):
        to_dos = ToDo.objects.all()
        not_complited = ToDo.objects.filter(complition=False).count()
        serializer = ToDoSerializer(to_dos, many = True)
        return render (request, 'main.html',{"todos":to_dos, 'not_complited':not_complited })

    def post(self, request):
        data = {
            'title':request.POST.get('title'),
            'text': request.POST.get('text'),
            'image':request.FILES.get('image'),
        }

        serializer = ToDoSerializer(data = data)
        if serializer.is_valid():
            to_do = serializer.save(author=request.user)
            return redirect(reverse('details', kwargs = {"id":to_do.id}))
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
class ToDoDetails(APIView):
    def get(self, request, todo_id):
        to_do = get_object_or_404(ToDo, id = todo_id)
        subtasks = to_do.subtasks.all()
        serializer = ToDoSerializer(to_do)
        serializerSubtask = SubtaskSerializer(subtasks, many =True)
        return render(request, 'details.html',{"todo":to_do,"subtasks":serializerSubtask.data})
    
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
                return redirect(f'{reverse("main")}?message=Successfully%20logged%20in')
            else:
                return Response({"error": "Incorrect login details"}, status=status.HTTP_401_UNAUTHORIZED)

        elif action == 'register':
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return render(request, 'login.html', {"user": serializer.data}, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)