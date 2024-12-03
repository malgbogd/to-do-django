from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect, render
from .models import ToDo, SubToDo
from .serializers import ToDoSerializer, UserSerializer, SubtaskSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
# def main(request):
#     to_dos = ToDo.objects.all()
#     return render (request, 'main.html',{"todos":to_dos})
def addToDo(request):
    return render(request, 'create.html')

def loginRegister(request):
    return render(request, 'login.html')


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
            'image':request.FILES.get('image')
        }

        serializer = ToDoSerializer(data = data)
        if serializer.is_valid():
            to_do = serializer.save()
            subtasks = to_do.subtasks.all()
            return redirect(reverse('details.html',{"id":to_do.id, "todo":to_do,"subtasks":subtasks}))
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
class ToDoDetails(APIView):
    def get(self, request, todo_id):
        to_do = get_object_or_404(ToDo, id = todo_id)
        subtasks = to_do.subtasks.all()
        serializer = ToDoSerializer(to_do)
        serializerSubtask = SubtaskSerializer(subtasks, many =True)
        return render(request, 'details.html',{"todo":to_do,"subtasks":serializerSubtask.data})
    
class UsersList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return render(serializer.data, 'login.html', status = status.HTTP_201_CREATED)
        else:
            pass