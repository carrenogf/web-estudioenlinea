# Generated by Django 3.2.4 on 2021-09-11 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contribuyente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=200)),
                ('Mensaje', models.TextField(blank=True, null=True)),
                ('url1', models.URLField(blank=True, null=True)),
                ('url2', models.URLField(blank=True, null=True)),
                ('url3', models.URLField(blank=True, null=True)),
                ('url4', models.URLField(blank=True, null=True)),
                ('url5', models.URLField(blank=True, null=True)),
                ('Contribuyente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contribuyente.contribuyente')),
            ],
        ),
    ]