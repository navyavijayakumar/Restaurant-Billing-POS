# Generated by Django 5.1.7 on 2025-03-13 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitems',
            old_name='product_obj',
            new_name='product_object',
        ),
    ]
