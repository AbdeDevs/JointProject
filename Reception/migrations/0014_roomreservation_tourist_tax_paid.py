# Generated by Django 5.0.3 on 2024-06-14 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0013_room_cleaner'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomreservation',
            name='tourist_tax_paid',
            field=models.BooleanField(default=False),
        ),
    ]
