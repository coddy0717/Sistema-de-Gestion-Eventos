# Generated by Django 5.1.5 on 2025-01-18 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_task_star_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='star_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
