# Generated by Django 5.1.2 on 2024-10-14 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0012_alter_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
