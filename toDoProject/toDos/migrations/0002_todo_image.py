# Generated by Django 5.1.3 on 2024-11-21 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='image',
            field=models.ImageField(blank='True', upload_to='images/'),
        ),
    ]
