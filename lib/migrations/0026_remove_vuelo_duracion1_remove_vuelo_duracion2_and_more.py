# Generated by Django 4.2.7 on 2024-02-19 20:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0025_vuelo_duracion1_vuelo_duracion2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vuelo',
            name='duracion1',
        ),
        migrations.RemoveField(
            model_name='vuelo',
            name='duracion2',
        ),
        migrations.AddField(
            model_name='historicoreserva',
            name='total',
            field=models.IntegerField(default=6500000, verbose_name='total'),
        ),
        migrations.AlterField(
            model_name='uservueloya',
            name='picture',
            field=models.ImageField(default='profile_pictures/default.png', upload_to='profile_pictures', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])]),
        ),
    ]
