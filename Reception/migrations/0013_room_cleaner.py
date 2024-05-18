# Generated by Django 5.0.3 on 2024-05-18 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0012_remove_worker_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='cleaner',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'cleaner'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Reception.worker'),
        ),
    ]
