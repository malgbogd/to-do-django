# Generated by Django 5.1.3 on 2024-12-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDos', '0012_alter_todo_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtodo',
            name='complition',
            field=models.BooleanField(default=False),
        ),
    ]
