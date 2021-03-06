# Generated by Django 3.2.4 on 2021-08-25 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribuyente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Razon_Social', models.CharField(max_length=200, verbose_name='Razón Social')),
                ('Cuit', models.IntegerField()),
                ('Actividades', models.TextField(blank=True, null=True, verbose_name='Actividades Económicas')),
                ('Fecha_inicio', models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio de Actividades')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono Celular')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('Usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contribuyente',
                'verbose_name_plural': 'Contribuyentes',
                'ordering': ['-created'],
            },
        ),
    ]
