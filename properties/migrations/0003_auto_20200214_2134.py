# Generated by Django 3.0.2 on 2020-02-14 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20200209_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
