# Generated by Django 5.1.3 on 2024-11-28 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDos', '0007_alter_todo_complition_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='complition_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]