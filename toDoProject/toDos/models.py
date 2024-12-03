from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    complition = models.BooleanField(default=False)
    complition_date = models.DateTimeField(blank = True, null=True)
    image = models.ImageField(upload_to='images/', blank ='True', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'to_dos')

    def __str__(self):
        return f'{self.title} | {self.creation_date}'

class SubToDo(models.Model):
    to_do = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=450)
    complition = models.BooleanField()

    def __str__(self):
        return f'{self.title} - subtask for {self.to_do}'
    
@receiver(post_save, sender = User)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
