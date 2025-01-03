# Generated by Django 5.1.3 on 2024-12-04 17:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDos', '0011_alter_subtodo_to_do_alter_todo_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='author',
            field=models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_dos', to=settings.AUTH_USER_MODEL),
        ),
    ]
