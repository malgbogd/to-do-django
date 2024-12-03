from django.contrib import admin
from .models import ToDo, SubToDo

# Register your models here.
class DisplayDate(admin.ModelAdmin):
    readonly_fields = ('creation_date',)
    
admin.site.register(ToDo,DisplayDate)
admin.site.register(SubToDo)