# Generated by Django 5.1.3 on 2024-11-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', models.TextField()),
                ('creation_date', models.DateTimeField()),
                ('complition', models.BooleanField()),
                ('complition_date', models.DateTimeField()),
            ],
        ),
    ]
