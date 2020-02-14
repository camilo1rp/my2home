# Generated by Django 3.0.2 on 2020-02-09 00:14

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.BigIntegerField(validators=[account.validators.validate_phone], verbose_name='phone'),
        ),
    ]