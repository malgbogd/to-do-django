# Generated by Django 5.1.3 on 2024-12-02 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDos', '0009_alter_subtodo_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtodo',
            name='to_do',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='toDos.todo'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='complition',
            field=models.BooleanField(default=False),
        ),
    ]
