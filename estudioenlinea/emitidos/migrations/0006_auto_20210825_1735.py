# Generated by Django 3.2.4 on 2021-08-25 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contribuyente', '0001_initial'),
        ('recibidos', '0003_alter_comprobantesrecibidos_contribuyente'),
        ('emitidos', '0005_alter_comprobantesemitidos_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprobantesemitidos',
            name='Contribuyente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contribuyente.contribuyente'),
        ),
        migrations.DeleteModel(
            name='Contribuyente',
        ),
    ]