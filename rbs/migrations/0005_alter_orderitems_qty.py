# Generated by Django 5.1.7 on 2025-03-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbs', '0004_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='qty',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=7),
        ),
    ]
