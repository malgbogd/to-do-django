from rest_framework import serializers, exceptions
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import ToDo, SubToDo
from django.contrib.auth.models import User

class ToDoSerializer(serializers.ModelSerializer):
    subtasks = serializers.PrimaryKeyRelatedField(many=True, queryset=SubToDo.objects.all(), required=False)
    class Meta:
        model = ToDo
        fields = ('id','title', 'text','creation_date','complition','complition_date','image','subtasks')

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubToDo
        fields = ('id','title','text','complition')

class UserSerializer(serializers.ModelSerializer):
    to_dos = serializers.PrimaryKeyRelatedField(many=True, queryset = ToDo.objects.all())
    
    email = serializers.EmailField(required = False, validators = [UniqueValidator(queryset = User.objects.all(), message = ['User with that email already exist.'])])
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'to_dos')
        extra_kwargs = {'password': {
            'write_only':True
        }}

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        try:
            validate_password(password)
        
        except ValidationError as e:
            raise exceptions.ValidationError({'password':e.messages})
        
        else:
            if email:
                user = User.objects.create_user(username=username, email = email, password=password)
            else:
                user = User.objects.create_user(username=username, password=password)
        return user