# Generated by Django 4.2.7 on 2024-01-22 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0022_oferta_delete_ofertas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservueloya',
            name='genero',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Prefiero no decir', 'Prefiero no decir')], default='No especificado', max_length=25),
        ),
    ]
