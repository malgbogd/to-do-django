from rest_framework import serializers, exceptions
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import ToDo, SubToDo, UserReward
from django.contrib.auth.models import User

class ToDoSerializer(serializers.ModelSerializer):
    subtasks = serializers.PrimaryKeyRelatedField(many=True, queryset=SubToDo.objects.all(), required=False)
    class Meta:
        model = ToDo
        fields = ('id','title', 'text','creation_date','completion','completion_date','image','subtasks','author')

class SubtaskSerializer(serializers.ModelSerializer):
    to_do = serializers.PrimaryKeyRelatedField(queryset=ToDo.objects.all())
    
    class Meta:
        model = SubToDo
        fields = ('id','to_do','title','text','completion')

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReward
        fields = ('id','user','image_url','date')


class UserSerializer(serializers.ModelSerializer):
    to_dos = serializers.PrimaryKeyRelatedField(many=True, queryset = ToDo.objects.all())
    
    email = serializers.EmailField(required = False, validators = [UniqueValidator(queryset = User.objects.all(), message = 'User with that email already exist.')])
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'to_dos')
        extra_kwargs = {'password': {
            'write_only':True,
            'required' : True
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