# Generated by Django 3.1.2 on 2021-05-29 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='Phone_No',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Zip_code',
            field=models.IntegerField(),
        ),
    ]
