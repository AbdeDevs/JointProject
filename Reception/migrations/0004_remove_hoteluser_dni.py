# Generated by Django 5.0.3 on 2024-03-26 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0003_hoteluser_id_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hoteluser',
            name='dni',
        ),
    ]
