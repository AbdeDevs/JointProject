# Generated by Django 5.0.3 on 2024-05-08 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cleaner', '0007_rename_cleaning_material_cleaningmaterial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cleanedroom',
            name='is_cleaned',
        ),
    ]
