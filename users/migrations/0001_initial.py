# Generated by Django 4.2.7 on 2023-12-18 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='user email')),
                ('fullname', models.CharField(max_length=100, verbose_name='full name')),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
