# Generated by Django 3.0.2 on 2020-01-28 19:23

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20191203_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, null=True, validators=[account.validators.validate_phone]),
        ),
    ]
