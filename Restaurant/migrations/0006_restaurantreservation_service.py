# Generated by Django 5.0.3 on 2024-04-28 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0005_rename_phone_externalrestaurantclient_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantreservation',
            name='service',
            field=models.CharField(choices=[('Esmorzar', 'Esmorzar'), ('Dinar', 'Dinar'), ('Sopar', 'Sopar')], default='None', max_length=15),
        ),
    ]
