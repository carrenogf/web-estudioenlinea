# Generated by Django 3.2.4 on 2021-08-04 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprobantesrecibidos',
            name='Tipo',
            field=models.CharField(max_length=60),
        ),
    ]
