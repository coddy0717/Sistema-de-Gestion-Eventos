# Generated by Django 5.1.5 on 2025-01-25 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_evento_ubicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='capacidad',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
