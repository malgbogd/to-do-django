# Generated by Django 5.1.3 on 2024-12-12 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDos', '0015_userrewards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrewards',
            name='image',
        ),
        migrations.AddField(
            model_name='userrewards',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
